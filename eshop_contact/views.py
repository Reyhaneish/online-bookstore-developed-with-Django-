from django.shortcuts import render
from .forms import ContactForm
from .models import ContactUs
from eshop_settings.models import SiteSettings
from django.contrib import messages


# Create your views here.

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    if contact_form.is_valid():
        full_name = contact_form.cleaned_data.get('full_name')
        email = contact_form.cleaned_data.get('email')
        subject = contact_form.cleaned_data.get('subject')
        text = contact_form.cleaned_data.get('text')
        ContactUs.objects.create(full_name=full_name, email=email, subject=subject, text=text, is_read=False)
        messages.success(request, "پیام شما با موفقیت ارسال شد!")
        contact_form = ContactForm()
    setting = SiteSettings.objects.first()
    context = {
        'contact_form': contact_form,
        'setting': setting
    }
    return render(request, 'contactus/contact_us.html', context)
