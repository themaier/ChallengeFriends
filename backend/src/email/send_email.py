import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from jinja2 import Template
from src.api_models.email import ChallengeEmail

load_dotenv(".env")


class Envs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME = os.getenv("MAIN_FROM_NAME")


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="./",
)


def send_email_background(
    background_tasks: BackgroundTasks, email_data: ChallengeEmail
):
    with open("./src/email/email.html.jinja") as f:
        tmpl = Template(f.read())
    html_content = tmpl.render(
        title="Challenge erhalten.",
        sent_to_username=email_data.send_to_username,
        sent_from_username=email_data.sent_from_username,
    )

    message = MessageSchema(
        subject="Challenge-Accepted",
        recipients=[email_data.send_to_email],
        body=html_content,
        subtype="html",
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
