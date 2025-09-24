import asyncio
import re
import sys
from email.message import EmailMessage
from pathlib import Path
from typing import Awaitable, Callable, Sequence

import aiosmtplib
import httpx
from dotenv import dotenv_values

sys.path.append(str(Path(__file__).parent))
from constants import EMAIL_BODY, EMAIL_SUBJECT, FORM_PAYLOAD, POST_URL

Fetcher = Callable[[int, httpx.AsyncClient], Awaitable[list[str]]]
config = dotenv_values(".env")


async def post_form_and_get_emails(
    page_number: int, client: httpx.AsyncClient
) -> list[str]:
    """
    Given a page number we make a request for it and return a list of emails.
    """
    payload = FORM_PAYLOAD.copy()
    payload.update({"c0-e7": f"number:{page_number}", "batchId": f"{page_number * 3}"})
    response = await client.post(POST_URL, data=payload)
    email_re = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    return email_re.findall(response.text)


async def fetch_all_emails(
    start: int = 1, end: int = 14, fetcher: Fetcher | None = None
) -> list[str]:
    """
    Hits all the pages from `start` to `end` and returns a flat list of emails.
    """
    fetcher = fetcher or post_form_and_get_emails

    async with httpx.AsyncClient() as client:
        tasks = [fetcher(page_number, client) for page_number in range(start, end + 1)]
        results = await asyncio.gather(*tasks)

    return [email for sublist in results for email in sublist]


async def send_email(to_address: str, mail_config: dict | None = None) -> tuple:
    """
    Sends the email using a google account with app password enabled.
    """
    cfg = {
        "port": 587, 
        "start_tls": True,
        "hostname": "smtp.gmail.com",
        "email_user": config["EMAIL_ACCOUNT"],
        "email_pass": config["EMAIL_PASS"],
    }

    if mail_config:
        cfg.update(mail_config)

    message = EmailMessage()
    message["From"] = cfg["email_user"]
    message["To"] = to_address
    message["Subject"] = EMAIL_SUBJECT
    message.set_content(EMAIL_BODY)

    response = await aiosmtplib.send(
        message,
        hostname=cfg["hostname"],
        port=cfg["port"],
        start_tls=cfg["start_tls"],
        username=cfg["email_user"],
        password=cfg["email_pass"],
    )
    return response[1]


async def send_bulk_emails(
    recipients: Sequence[str], sending_function: Callable[[str], Awaitable[str]]
) -> None:
    """
    Async loop all the emails.
    """
    sem = asyncio.Semaphore(20)

    async def _bounded_send(to_address: str):
        async with sem:
            return await sending_function(to_address)

    tasks = [_bounded_send(r) for r in recipients]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def main():  # pragma: no cover
    all_emails = await fetch_all_emails(1, 14)
    await send_bulk_emails(all_emails, send_email)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
