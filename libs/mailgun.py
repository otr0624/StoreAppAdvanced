from typing import List
from requests import Response, post

class Mailgun:
    MAILGUN_DOMAIN = "sandboxec53074368814fa0ba8c880269cac21e.mailgun.org"
    MAILGUN_API_KEY = "e1b75e8d80341924884aa05ec6c68d1d-f135b0f1-3a521536"

    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = "mailgun@sandboxec53074368814fa0ba8c880269cac21e.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        return post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )