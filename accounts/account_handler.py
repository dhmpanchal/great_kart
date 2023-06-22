from extras.email_handler import EmailHandler
from .models import Account, UserProfile


class AccountHandler(object):

    def __init__(self, *args, **kwargs):
        super(AccountHandler, self).__init__(*args, **kwargs)
        self.created = False

    def create_account(self, current_site, form=None):
        if form is not None and form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name,username=username,
                                                email=email, password=password)
            user.phone = phone
            user.save()

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.save()
            
            # send activation link 
            email_handler = EmailHandler()
            email_handler.send_activation_mail(current_site, user)
            email_handler.send_email()
            self.created = True
        else:
            self.created = False

        return self.created