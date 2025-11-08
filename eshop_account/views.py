from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')  # برای اینکه به لینک صفحه لاگین دسترسی نداشته باشد

    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            login_form.add_error('username', "نام کاربری یا رمز عبور نادرست است.")

    context = {'login_form': login_form}
    return render(request, 'account/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')  # برای اینکه به لینک صفحه لاگین دسترسی نداشته باشد

    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('/login')

    context = {
        'register_form': register_form
    }
    return render(request, 'account/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def user_account_main_page(request):
    user = request.user  # دسترسی به اطلاعات کاربر
    context = {
        'user': user,
    }
    return render(request, 'account/user_account_main.html', context)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
@login_required(login_url='/login')
def edit_user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات پروفایل شما با موفقیت به‌روزرسانی شد.')
            return redirect('/user/edit')
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'account/edit-profile.html', context)

def user_sidebar(request):
    context = {}
    return render(request, 'account/user-sidebar.html', context)
