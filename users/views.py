from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, StatusUpgradeForm
from .models import Profile
from django.contrib.auth import login
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            # Добавляем отладочную информацию
            print("Form errors:", form.errors)
            print("Form data:", form.data)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    # Явно получаем профиль через get_or_create для избежания ошибок
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user_profile  # Используем полученный профиль
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def upgrade_status(request):
    # Убеждаемся, что профиль существует
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = StatusUpgradeForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['new_status']

            # Проверяем, что новый статус выше текущего
            status_order = {'regular': 0, 'advanced': 1, 'vip': 2}
            if status_order[new_status] > status_order[user_profile.status]:
                user_profile.status = new_status
                user_profile.save()
                messages.success(request, 'Статус успешно обновлен!')
            else:
                messages.warning(request, 'Вы не можете понизить свой статус!')

            return redirect('profile')
    else:
        form = StatusUpgradeForm()

    return render(request, 'users/upgrade_status.html', {'form': form})