from app.database.models.user import User
from app.core.config import settings
import smtplib


def send_email(msg: str, user: User):
    with smtplib.SMTP(host='smtp.office365.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user=settings.MANAGEMENT_EMAIL, password=settings.MANAGEMENT_EMAIL_PASSWORD)
        smtp.sendmail(settings.MANAGEMENT_EMAIL, user.email, msg)
