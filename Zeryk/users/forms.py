from django import forms
from .models import AUser as User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile_picture = self.cleaned_data.get('profile_picture')

        if commit:
            user.save()
        return user