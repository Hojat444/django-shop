# Sending email(not in tutorial)

from django.core.mail import EmailMessage

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")  # Update with your project's settings module
django.setup()

subject = 'Test from django app'
message = 'This is only a test from django shop application.'
from_email = 'h.ansari2001@gmail.com'
recipient_list = ['m.amin.ansari@gmail.com']



email = EmailMessage(subject, message, from_email, recipient_list)
email.attach_file('/Users/hojat/Desktop/django-shop/myshop/media/products/2022/11/09/e9832a15f1c62c15398a36318cd0186c5e8276e0_1605622481.jpg')  # Update the path to your image file
email.send()