from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

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
    pfp = forms.ImageField(required=False,
                           widget=forms.FileInput(attrs={'class': 'form-control',
                                                         'id': 'pfp',
                                                        }))
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'pfp']

    def clean_pfp(self):
        pfp = self.cleaned_data.get('pfp')
        if not pfp:
            if self.instance.pk:
                return self.instance.userprofile.get_default_pfp()
        return pfp

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['pfp']

    def clean_pfp(self):
        pfp = self.cleaned_data.get('pfp')
        if not pfp:
            return self.instance.get_default_pfp()
        return pfp

class PasswordChangeForm(forms.ModelForm):
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
    class Meta:
        model = User
        fields = ['password1', 'password2']
