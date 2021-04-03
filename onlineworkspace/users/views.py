from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Profile, Product


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}, Please log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    left_workspaces = request.user.profile.workspaces_number
    left_files = request.user.profile.files_number

    context = {
        'workspaces': left_workspaces,
        'files': left_files
    }

    return render(request, 'users/profile.html', context)
