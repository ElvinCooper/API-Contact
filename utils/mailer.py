import requests, os
from flask import render_template
from dotenv import load_dotenv

load_dotenv()

# def send_simple_email_message(to_email, subject, template_name, **template_vars):
#     domain  = os.getenv("MAILGUN_DOMAIN")
#     api_key = os.getenv("MAILGUN_API_KEY")
#     sender  = os.getenv("MAILGUN_FROM")

#     html_body = render_template(f"emails/{template_name}.html", **template_vars)

#     return requests.post(
#         f"https://api.mailgun.net/v3/{domain}/mesages",
#         auth=("api", api_key),
#         data={"from": sender,
#               "to": to_email,
#               "subject": subject,
#               "text": html_body
#         }
#     )