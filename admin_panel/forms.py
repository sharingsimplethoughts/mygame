from django import forms
from django.contrib.auth.models import User
from registration.models import *


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    def clean(self):
        email = self.cleaned_data.get('email')
        userA = User.objects.filter(email=email, is_staff=True, is_superuser=True)
        user = userA.exclude(email__isnull=True).exclude(email__iexact='').distinct()
        if user.exists() and user.count() == 1:
            userObject = user.first()
        else:
            raise forms.ValidationError("User with this E-mail is not exist")
        password = self.cleaned_data.get('password')
        check_pass = userObject.check_password(password)
        if check_pass:
            if not userObject.is_staff or not userObject.is_active:
                raise forms.ValidationError('Your have not permission to access this panel')
            return self.cleaned_data
        raise forms.ValidationError('Your password is incorrect')


class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField()
    password = forms.CharField()
    confpassword = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].strip = False
        self.fields['password'].strip = False
        self.fields['confpassword'].strip = False

    def clean(self):
        password = self.cleaned_data.get('password')
        confpassword = self.cleaned_data.get('confpassword')

        print(len(password))
        if not len(password) >= 8 or not len(confpassword) >= 8:
            raise forms.ValidationError('Password must be at least 8 characters')

        oldpassword = self.cleaned_data.get('oldpassword')
        if not self.user.check_password(oldpassword):
            raise forms.ValidationError('Incorrect old password')

        if password != confpassword:
            raise forms.ValidationError('Both password fields should be same')

        return self.cleaned_data


class AdminProfileEditForm(forms.Form):
    email = forms.CharField()
    mobile_number = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AdminProfileEditForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not self.user.email == email:

            if email.count('@') > 1:
                raise forms.ValidationError('Please enter a valid email')

            user_qs = User.objects.filter(email__iexact=email, account_type="1")

            if user_qs.exists():
                raise forms.ValidationError('User with this Email already exist')
            return email

        return email

    def clean_mobile_number(self):

        mobile_number = self.cleaned_data.get('mobile_number')

        if mobile_number.isdigit() and len(mobile_number) < 12:
            obj = RegisteredUser.objects.get(user=self.user)

            if not obj.mobile == mobile_number:
                user_qs = RegisteredUser.objects.filter(mobile__iexact = mobile_number)
                if user_qs.exists():
                    raise forms.ValidationError('User with this phone number already exist')
                return mobile_number
            return mobile_number
        raise forms.ValidationError('Please correct your Mobile number')


def is_whitespaces(string):
    string_a = string.replace('&nbsp;', '')
    string_b = 	string_a.replace('<p>' , '')
    string_c = 	string_b.replace('</p>' , '')
    string_d = string_c.replace('\r\n' , '')
    string_e = string_d.strip()
    if string_e =='':
        return True
    else:
        return False


