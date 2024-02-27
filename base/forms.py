from django.forms import ModelForm
from django import forms
from .models import Room
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Nova senha', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirmar nova senha', widget=forms.PasswordInput, required=False)

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'username', 'email', 'bio']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
