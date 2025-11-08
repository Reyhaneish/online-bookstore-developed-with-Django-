from django import forms
from django.contrib.auth.models import User
from django.core import validators

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your username'}),
                               label='username',
                               )


    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'enter your password'}),
                               label='password')

#####################


    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exists_user = User.objects.filter(username=username).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربر ثبت نام نکرده است')
        return username


class RegisterForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your username'}),
    label='username',
    validators=[
        validators.MaxLengthValidator(limit_value=20,message= 'تعداد کاراکتر حداکثر 20 تا قبول میکنم'),
        validators.MinLengthValidator(limit_value=8, message='تعداد کاراکتر حداقل 8 تا قبول میکنم')
                             ]
                             )

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'enter your password'}),
    label='password')

    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your email'}),
    label='email',
    validators=[
        validators.EmailValidator('ایمیل معتبر نیست')
    ]
                             )

    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'enter your repassword'}),
    label='re-password')

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("re_password")

        if password != confirm_password:
            raise forms.ValidationError("رمز عبور و تکرار آن باید یکسان باشند.")

        return password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("کاربر قبلاً ثبت نام کرده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت نام شده است.")
        return email