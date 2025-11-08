from django.urls import path
from .views import contact_page
app_name='eshop_contact'

urlpatterns=[
    path('contactus/',contact_page,name='contactus')
]