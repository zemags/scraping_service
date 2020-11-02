from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


User = get_user_model()


def login_view(request):
    # user authentication
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return  redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)  # presetup users password, creating instance
        new_user.set_password(form.cleaned_data['password'])  # hash password
        new_user.save()
        messages.success(request, 'Successfully registered.')
        return render(request, 'accounts/register_done.html', context={'new_user': new_user})
    return render(request, 'accounts/register.html', context={'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Successfully updated.')
                return redirect('accounts:update')
        form = UserUpdateForm(initial={'city': user.city, 'language': user.language, 'send_email': user.send_email})
        return render(request, 'accounts/update.html', context={'form': form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)  # from db get user with id == pk (pk is current user id)
            qs.delete()
            messages.warning(request, 'User removed.')
    return redirect('home')