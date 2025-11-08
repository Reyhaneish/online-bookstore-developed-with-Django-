from django import forms
from django.core import validators

class ContactForm(forms.Form):  # باید از forms.Form استفاده کنید
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی را وارد کنید','class':'form-control'}),
        label='نام و نام خانوادگی',
        validators=[
            validators.MaxLengthValidator(150, 'نام نام خانوادگی شما نمیتواند بیش از 150 کاراکتر باشد')
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل را وارد کنید','class':'form-control'}),
        label='ایمیل',
        validators=[
            validators.MaxLengthValidator(100, 'ایمیل شما نمیتواند بیش از 100 کاراکتر باشد')
        ]
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'عنوان پیام را وارد کنید','class':'form-control'}),
        label='عنوان پیام',
        validators=[
            validators.MaxLengthValidator(200, 'عنوان پیام شما نمیتواند بیش از 200 کاراکتر باشد')
        ]
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'متن پیام را وارد کنید','class':'form-control','rows':'80'}),
        label='متن پیام',
    )
