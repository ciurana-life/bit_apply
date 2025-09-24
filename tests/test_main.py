import asyncio
from typing import Sequence

import httpx
import pytest
import vcr

from bit_apply.main import (
    fetch_all_emails,
    post_form_and_get_emails,
    send_bulk_emails,
    send_email,
)


@vcr.use_cassette("fixtures/vcr_cassettes/test_post_form_and_get_emails.yaml")
@pytest.mark.asyncio
async def test_post_form_and_get_emails():
    async with httpx.AsyncClient() as client:
        email_list = await post_form_and_get_emails(4, client)
        assert "test@victorciurana.com" in email_list
        assert len(email_list) == 9


@pytest.mark.asyncio
async def test_fetch_all_emails():
    async def fake_fetcher(page_number, client):
        await asyncio.sleep(0)
        return [f"user{page_number}@example.com"]

    emails = await fetch_all_emails(start=1, end=3, fetcher=fake_fetcher)

    assert emails == [
        "user1@example.com",
        "user2@example.com",
        "user3@example.com",
    ]


@pytest.mark.asyncio
async def test_send_email():
    # Requires mailhog running !
    cfg = {
        "port": 1025,
        "start_tls": False,
        "hostname": "127.0.0.1",
        "email_user": "test",
        "email_pass": "test",
    }
    email_response = await send_email("test@test.com", mail_config=cfg)
    assert "Ok" in email_response


@pytest.mark.asyncio
async def test_send_bulk_emails():
    async def fake_send(email: str) -> str:
        await asyncio.sleep(0)
        if email == "fail@test.com":
            raise ValueError("Simulated failure")
        return f"sent:{email}"

    emails: Sequence[str] = ["a@test.com", "b@test.com", "fail@test.com"]
    results = await send_bulk_emails(emails, fake_send)

    assert results[0] == "sent:a@test.com"
    assert results[1] == "sent:b@test.com"
    assert isinstance(results[2], Exception)
    assert str(results[2]) == "Simulated failure"
