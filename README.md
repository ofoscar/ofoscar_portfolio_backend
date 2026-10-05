# OFOSCAR Portfolio Backend

Production-ready backend for managing the projects displayed on my personal portfolio.

Built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **AWS S3**, **Docker**, and **GitHub Actions**.

The application exposes public project data for the portfolio while protecting administrative operations such as creating, updating, deleting projects, and uploading images.

---

## Features

- JWT-based admin authentication
- Protected admin endpoints
- Project CRUD operations
- Partial project updates with `PATCH`
- Project tags
- Cover images
- Project image galleries with descriptions
- Image uploads to AWS S3
- Automatic S3 cleanup when images are replaced or removed
- PostgreSQL persistence
- Alembic database migrations
- Health check endpoint
- Dockerized application
- Automated CI/CD with GitHub Actions
- Docker images published to GitHub Container Registry
- Deployment to AWS EC2
- HTTPS via Caddy
- AWS IAM role authentication for S3 in production
- AWS Systems Manager deployment without exposing SSH to CI

---

## Tech Stack

### Backend

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy 2
- Alembic
- PostgreSQL
- Psycopg2
- PyJWT
- pwdlib / Argon2
- Boto3

### Infrastructure

- Docker
- Docker Compose
- GitHub Actions
- GitHub Container Registry
- AWS EC2
- AWS S3
- AWS IAM
- AWS Systems Manager
- Caddy

---

## Architecture

```text
                    ┌──────────────────────┐
                    │     Portfolio UI     │
                    │      Next.js         │
                    └──────────┬───────────┘
                               │
                               │ HTTPS
                               ▼
                    ┌──────────────────────┐
                    │        Caddy         │
                    │   Reverse Proxy/TLS  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │   Portfolio Backend  │
                    └───────┬───────┬──────┘
                            │       │
                   SQL      │       │ S3 API
                            ▼       ▼
                  ┌────────────┐  ┌────────────┐
                  │ PostgreSQL │  │   AWS S3   │
                  └────────────┘  └────────────┘
```

---

## API Overview

### Authentication

```http
POST /auth/login
GET  /auth/me
```

### Projects

```http
GET    /projects
GET    /projects/{project_id}
POST   /projects
PATCH  /projects/{project_id}
DELETE /projects/{project_id}
```

Administrative write operations require authentication.

### Uploads

```http
POST /uploads/images
```

Uploads are stored in AWS S3 and the generated public URL can be assigned to a project's cover image or gallery.

Example response:

```json
{
  "status": "ok",
  "database": "ok"
}
```

---

## Project Model

A project contains data such as:

```json
{
  "id": 1,
  "title": "Example Project",
  "hook": "Project hook",
  "description": "Project description",
  "github_url": "https://github.com/...",
  "demo_url": "https://example.com",
  "cover_image_url": "https://...",
  "published": true,
  "tags": [
    "FastAPI",
    "Next.js",
    "PostgreSQL"
  ],
  "images": [
    {
      "id": 1,
      "image_url": "https://...",
      "description": "Project dashboard"
    }
  ]
}
```

Tags are validated and limited in length.

---

## Authentication

Authentication uses OAuth2 password flow with JWT bearer tokens.

Passwords are hashed using Argon2 and are never stored as plaintext.

Protected requests use:

```http
Authorization: Bearer <access_token>
```

The application currently uses a single admin account because the API is designed specifically for managing a personal portfolio.

---

## Local Development

### Requirements

- Python 3.12+
- `uv`
- Docker
- Docker Compose
- AWS CLI configured locally
- Access to an S3 bucket

### Clone the repository

```bash
git clone https://github.com/ofoscar/ofoscar_portfolio_backend.git
cd ofoscar_portfolio_backend
```

### Install dependencies

```bash
uv sync
```

### Environment variables

Create:

```text
.env.app
```

Example:

```env
SECRET_KEY=
ADMIN_EMAIL=
ADMIN_PASSWORD_HASH=

DATABASE_URL=postgresql+psycopg2://ofoscar:password@localhost:5433/ofoscar

AWS_REGION=
S3_BUCKET_NAME=
S3_PUBLIC_URL=
```

Do not commit real secrets.

The repository should only contain an `.env.example` file.

---

## Local PostgreSQL

Start PostgreSQL with Docker Compose:

```bash
docker compose --env-file .env.docker up -d
```

Example `.env.docker`:

```env
POSTGRES_DB=ofoscar
POSTGRES_USER=ofoscar
POSTGRES_PASSWORD=
```

Apply migrations:

```bash
uv run alembic upgrade head
```

---

## Run the API

Development mode:

```bash
uv run fastapi dev src/ofoscar_backend/main.py
```

API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Testing

Run:

```bash
uv run pytest
```

Tests run against PostgreSQL in CI.

GitHub Actions starts a temporary PostgreSQL service, applies Alembic migrations, and then runs the test suite.

---

## Database Migrations

Create a migration:

```bash
uv run alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

Check current revision:

```bash
uv run alembic current
```

---

## Docker

Build locally:

```bash
docker build -t ofoscar-backend .
```

Run:

```bash
docker run \
  --env-file .env.app \
  -p 8000:8000 \
  ofoscar-backend
```

---

## CI/CD

The GitHub Actions pipeline runs automatically on pushes to the main development branch.

```text
Push
  ↓
PostgreSQL service
  ↓
Alembic migrations
  ↓
Pytest
  ↓
Docker build
  ↓
Push image to GHCR
  ↓
AWS OIDC authentication
  ↓
AWS Systems Manager
  ↓
EC2 deployment
```

The production container image is published to:

```text
ghcr.io/ofoscar/ofoscar-portfolio-backend
```

Production deployment performs:

```bash
docker compose pull
docker compose run --rm api alembic upgrade head
docker compose up -d
```

No long-lived AWS credentials or SSH private keys are required by the deployment workflow.

---

## Production

Production API:

```text
https://api.ofoscar.com
```

### Production services

```text
AWS EC2
├── Caddy
├── FastAPI
└── PostgreSQL

AWS S3
└── Portfolio images
```

The API container authenticates to AWS using the EC2 IAM role rather than static AWS credentials.

---

## Security

The project follows several production-oriented security practices:

- Secrets are excluded from Git
- Passwords are hashed with Argon2
- JWTs are signed with a strong secret
- Protected routes require Bearer authentication
- PostgreSQL is not exposed publicly
- FastAPI port `8000` is not exposed directly to the internet
- Public traffic is served through HTTPS
- AWS S3 access uses IAM
- EC2 production deployment uses GitHub OIDC
- GitHub Actions deploy through AWS Systems Manager instead of public SSH access
- IAM policies can be scoped to least privilege

---

## Repository Structure

```text
.
├── alembic/
├── src/
│   └── ofoscar_backend/
│       ├── core/
│       ├── database/
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       ├── services/
│       └── main.py
├── tests/
├── .github/
│   └── workflows/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
└── uv.lock
```

---

## Roadmap

Potential future improvements:

- More complete automated test coverage
- Deployment rollback support
- Structured application logging
- Monitoring and alerting
- Rate limiting
- Project ordering
- Draft/public project separation
- Image optimization
- Automated backups
- API versioning

---

## Author

**Oscar Ramirez Angulo**

Full Stack Developer

- Portfolio: https://ofoscar.com
- GitHub: https://github.com/ofoscar
- API: https://api.ofoscar.com

---

## License

This project is currently intended for personal portfolio use.

If you plan to reuse or distribute the code, add an explicit open-source license such as MIT.
