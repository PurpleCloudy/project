from django import forms
from django.contrib.auth import get_user_model
from .models import UserInformation

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя')
    password = forms.CharField(label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__password'
            }
        )
    )
    
    def clean_username(self):
        profile = self.cleaned_data.get('username')
        queryset = User.objects.filter(username__iexact = profile)

        if not queryset.exists():
            raise forms.ValidationError("This user doesn't exist")

        return profile

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = [
            'bio',
            'profile_image',
        ]

class RegisterForm(forms.Form):
    username = forms.CharField(required = True, label='Имя')
    email = forms.EmailField(required=True, label='Email')
    password = forms.CharField(required = True, label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__password'
            }
        )
    )

    def clean_username(self):
        profile = self.cleaned_data.get('username')
        queryset = User.objects.filter(username__iexact = profile)

        if queryset.exists():
            raise forms.ValidationError('Invalid username')

        return profile