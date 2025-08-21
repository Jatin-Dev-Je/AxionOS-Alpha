import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Basic configuration via environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Database URL: use Postgres if provided, else local SQLite for quick start
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./axionos.db")

# SMTP / Email (placeholder; for future email sending)
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "0") or 0)
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "no-reply@example.com")

# Password policy (basic defaults)
MIN_PASSWORD_LENGTH = int(os.getenv("MIN_PASSWORD_LENGTH", "8"))

# App base URL (used to build password reset links)
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:3000")

