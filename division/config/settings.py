import os
from dotenv import load_dotenv

load_dotenv()

DATEFMT: str = "%d/%m/%Y %H:%M:%S"
ROOT_PATH: str = os.path.dirname(__file__)

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 8025))
SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", 5))
EMAIL_FROM: str = os.getenv("EMAIL_FROM")

SECRET_KEY: str = os.getenv("SECRET_KEY", "")
ALGORITHM: str = os.getenv("ALGORITHM", "")

# DATABASE_PATH: str = os.path.join(ROOT_PATH, "..", "assets", "database.db")
DATABASE_PATH = "/home/scorel/Documents/projects/poli_dti/dti_server/assets/database.db"
DATABASE_URI = os.getenv("DATABASE_URI", f"sqlite:///{DATABASE_PATH}")

DEFAULT_EXPIRATION_TIME = int(os.getenv("DEFAULT_EXPIRATION_TIME", 8784))
