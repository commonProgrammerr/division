"""Settings module"""

import os
from dotenv import load_dotenv
# from dynaconf import Dynaconf

HERE = os.path.dirname(os.path.abspath(__file__))

# settings = Dynaconf(
#     envvar_prefix="division",
#     preload=[os.path.join(HERE, "default.toml")],
#     settings_files=["settings.toml", ".secrets.toml"],
#     environments=["development", "production", "testing"],
#     env_switcher="division_env",
#     load_dotenv=True,
# )

load_dotenv()


class Config:
    # DATABASE_PATH: str = os.path.join(ROOT_PATH, "..", "assets", "database.db")
    DATABASE_PATH = os.path.join(HERE, "../../assets/database.db")
    DATABASE_URI = os.getenv("DATABASE_URI", f"sqlite:///{DATABASE_PATH}")

    MQTT_HOST: str = os.getenv("MQTT_HOST")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

    DEFAULT_EXPIRATION_TIME = int(os.getenv("DEFAULT_EXPIRATION_TIME", 8784))

    class Security:
        # Set secret key in .secrets.toml
        # SECRET_KEY = ""
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 600
        REFRESH_TOKEN_EXPIRE_MINUTES = 600
        RESET_TOKEN_EXPIRE_MINUTES = 10
        PWD_RESET_URL = "https://dm.com/reset_password"

    security = Security()

    class Email:
        debug_mode = True
        smtp_sender = "no-reply.divisor@poli.br"
        smtp_server = "localhost"
        smtp_port = 1025
        smtp_user = "<replace in .secrets.toml>"
        smtp_password = "<replace in .secrets.toml>"

    email = Email()

    class Redis:
        host = "redis"
        port = 6379

    redis = Redis()

    class SessionStore:
        host = "@get redis.host"
        port = "@get redis.port"
        db = 1
        expiration = "@int @jinja {{60 * 60 * 24 * 7}}"

    session_store = SessionStore()


settings = Config()
