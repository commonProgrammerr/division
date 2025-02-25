import re
import smtplib
from email.mime.text import MIMEText

from division.config.settings import SMTP_HOST, SMTP_PORT, SMTP_TIMEOUT
from division.utils.logger import get_logger

log = get_logger()

EMAIL_REGEX = (
    r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
    r"\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")"
    r"@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|"
    r"\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}"
    r"(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:"
    r"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
)


def check_valid_email(address):
    """Check if an email address is valid.

    Returns: True if valid, False otherwise.
    """
    return bool(re.fullmatch(EMAIL_REGEX, address))


def send_email(from_, to, subject, body):
    if not isinstance(to, list):
        to = [to]

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            message = MIMEText(body)
            message["From"] = from_
            message["To"] = ",".join(to)
            message["Subject"] = subject
            server.sendmail(from_, to, message.as_string())
    except Exception:
        log.error("Error sending email to %s", ", ".join(to))
