# README

## Objetivo
Hay muchas empresas en el ParcBit, muchas de ellas del sector tecnológico.  
El objetivo de este repositorio es enviar correos electrónicos a estas empresas para buscar oportunidades como programador.


### Instalación

Poetry: https://python-poetry.org/docs/#installation

Docker: https://docs.docker.com/get-docker/

Instalar dependencias del proyecto:
```bash
poetry install
```

### Configuración de Email

Crea un archivo .env en la raíz con:
```bash
EMAIL_PASS="tu_contrasenya_app"
EMAIL_ACCOUNT="tu_correo@gmail.com"
```

Necesitas una contraseña de aplicación de Google (App Password).

Prueba con MailHog
```bash
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

Visita http://localhost:8025 para ver los correos enviados.


### Notas técnicas

* Async / httpx: solicitudes concurrentes.
* VCR.py: para pruebas offline de requests.
* CI / GitHub Actions: corre linting, tests y coverage.
* Ruff / Black / Isort: formateo y linting automáticos.
