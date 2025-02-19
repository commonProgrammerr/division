import os
from dotenv import load_dotenv

load_dotenv()

DATEFMT: str = "%d/%m/%Y %H:%M:%S"
ROOT_PATH: str = os.path.dirname(__file__)
DATABASE_PATH: str = os.path.join(ROOT_PATH, "..", "assets", "database.db")

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 8025))
SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", 5))
EMAIL_FROM: str = os.getenv("EMAIL_FROM")


DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")
