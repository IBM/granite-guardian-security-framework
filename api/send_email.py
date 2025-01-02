# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()


def send_email(
    risk_type,
    name="Yash Sawlani",
    email="yash.sawlani@ibm.com",
):
    message = Mail(
        from_email="ysawibm@gmail.com",
        to_emails="yash.sawlani@ibm.com",
        subject=f"{risk_type} Risk Detected In Guardian AI",
        plain_text_content=f"{risk_type} risk detected by Guardian AI from User - {name}, Email - {email}. \n Please review the prompt and take necessary actions. \n\n This action is logged in the risk management database",
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
