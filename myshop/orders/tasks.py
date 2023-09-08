from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order  # Import your Order model
import weasyprint

@shared_task
def send_order_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'My shop - Your Order'
    message = 'Thank you for your order!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [order.email]  # Replace with appropriate recipient email

    # Generate PDF using your existing function
    html = render_to_string('orders/order/pdf.html', {"order": order})
    pdf_file = weasyprint.HTML(string=html).write_pdf(stylesheets=[weasyprint.CSS(
        settings.STATIC_ROOT + 'css/pdf.css'
    )])

    # Attach PDF to the email
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(f'order_{order.id}.pdf', pdf_file, 'application/pdf')

    # Send the email
    email.send()
