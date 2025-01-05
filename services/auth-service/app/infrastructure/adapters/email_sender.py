from email.message import EmailMessage

import aiosmtplib

from app.application.interfaces.email_sender_interface import EmailSender


class SMTPEmailSender(EmailSender):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._username = username
        self._password = password

    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        # Создаем объект сообщения
        message = EmailMessage()
        message["From"] = self._username
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        # Отправляем письмо через aiosmtplib
        try:
            print(f"Attempting to send email to {recipient}")
            await aiosmtplib.send(
                message,
                hostname=self._smtp_server,
                port=self._smtp_port,
                username=self._username,
                password=self._password,
            )
            print(f"Email sent successfully to {recipient}")
        except Exception as e:
            print(f"Error sending email to {recipient}: {e}")
