from django.core.mail import EmailMessage, send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from greatkart import settings


class EmailHandler(object):

    def __init__(self, *args, **kwargs):
        super(EmailHandler, self).__init__(*args, **kwargs)
        self.email_subject = None
        self.email_content = None
        self.email_recipient = []
        self.email_from = settings.EMAIL_HOST_USER
        self.tls = settings.EMAIL_USE_TLS

    def send_activation_mail(self, current_site, user):
        self.email_subject = "Account Activation"
        context = {
            'user': user,
            'domain': current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        }

        template = render_to_string('email/account_activation_mail.html', context)

        self.email_recipient.append(user.email)
        self.email_content = template
    
    def send_forgot_password_mail(self, current_site, user, email):
        self.email_subject = "Reset Password"
        context = {
            'user': user,
            'domain': current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        }

        template = render_to_string('email/forgot_password_email.html', context)

        self.email_recipient.append(email)
        self.email_content = template
    
    def send_order_recieved_mail(self, user, email, order):
        self.email_subject = "your order has been received"
        context = {
            'user': user,
            'order': order,
        }

        template = render_to_string('email/order_recieved.html', context)

        self.email_recipient.append(email)
        self.email_content = template

    def send_email(self):
        if self.email_content is None:
            raise ValueError("Email setup not performed, no email content set")
        elif len(self.email_recipient) == 0:
            raise ValueError("No recipient set for outgoing email")
        else:
            try:
                send_mail(
                    subject=self.email_subject,
                    message=self.email_content,
                    from_email=self.email_from,
                    recipient_list= self.email_recipient,
                    fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
                )
                print("Email sent successfully!")
            except Exception as e:
                print(f"Error in sending mail:: {e}")