from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': None,
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class StatusUpgradeForm(forms.Form):
    NEW_STATUS_CHOICES = [
        ('advanced', 'Продвинутый ($50)'),
        ('vip', 'VIP ($100)'),
    ]

    new_status = forms.ChoiceField(
        choices=NEW_STATUS_CHOICES,
        widget=forms.RadioSelect,
        label="Выберите новый статус"
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Обновляем или создаем профиль
            profile, created = Profile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data.get('phone', ''),
                    'address': self.cleaned_data.get('address', '')
                }
            )
        return user