from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging
from celery import shared_task


@shared_task
def send_email(user_email, user_name, order_id, order_status):
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=user_email,
        subject=f'Order {order_id} has been {order_status}',
        html_content=f'Dear {user_name}, <br> Your order {order_id} has been {order_status}. <br> Thanks, <br> '
                     f'BrewUnifed Team'
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"Email sent successfully for order {order_id}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending email for order {order_id}. Error: {e}")
