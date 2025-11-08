from django.urls import path
from .views import login_user,register,logout_page,user_account_main_page,edit_user_profile
app_name='account'

urlpatterns = [
    path('login/',login_user,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout_page,name='logout'),
    path('user/',user_account_main_page,name='user_account'),
    path('user/edit/',edit_user_profile,name='edit-profile'),

    ]