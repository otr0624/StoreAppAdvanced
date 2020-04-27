def send_confirmation_email(self) -> Response:
    link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)

    return post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
            "to": self.email,
            "subject": "Registration confirmation",
            "text": f"Please click the link to confirm your registration: {link}",
        },
    )