from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import NewUserForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New account created for: {username}')
            login(request, user)
            messages.info(request, f'You are now logged in as: {username}')
            return redirect('main:home')
        else:
            for error, msg in form.error_messages.items():
                messages.error(request, f'{error}: {msg}')
            form = NewUserForm(request.POST)
    else:
        form = NewUserForm()

    return render(request,
                  'account/register.html',
                  context={'form': form})


@login_required
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'account/profile.html', context)
    return render(request, 'account/profile.html', context)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as: {username}')
                return redirect('main:home')
            else:
                messages.error(request, 'The username or password that you entered was invalid.')
    else:
        form = AuthenticationForm()
    return render(request,
                  'account/login.html',
                  context={'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('main:home')
