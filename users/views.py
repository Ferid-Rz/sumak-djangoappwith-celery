from django.shortcuts import render, redirect
from .forms import RegistrateOurUser, UpdateOurProfile, ProfileImage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegistrateOurUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был создан, введите имя и пароль для авторизации')
            return redirect('user')
    else:
        form = RegistrateOurUser()
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        img_profile = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
        update_user = UpdateOurProfile(request.POST, instance=request.user)

        if update_user.is_valid() and img_profile.is_valid():
            update_user.save()
            img_profile.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлен')
            return redirect('profile')
    else:
        img_profile = ProfileImage(instance=request.user.profile)
        update_user = UpdateOurProfile(instance=request.user)


    data = {
        'img_profile' : img_profile,
        'update_user' : update_user
    }

    return render(request, 'users/profile.html', data)
