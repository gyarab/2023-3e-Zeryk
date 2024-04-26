from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

#tato třída je určena k registraci uživatelů, pravděpodobně v rámci webové aplikace
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
    
    #specifikuje model (User) a pole, která mají být zahrnuta ve formuláři
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'pfp']

    #tato metoda slouží k čištění a ověřování pole pfp.
    def clean_pfp(self):
        pfp = self.cleaned_data.get('pfp')
        if not pfp:
            if self.instance.pk:
                return self.instance.userprofile.get_default_pfp()
        return pfp

#účelem této třídy je aktualizovat informace o uživateli, konkrétně v tomto případě uživatelské jméno.
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

#tato třída slouží k aktualizaci profilového obrázku uživatele.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['pfp']

    def clean_pfp(self):
        pfp = self.cleaned_data.get('pfp')
        if not pfp:
            return self.instance.get_default_pfp()
        return pfp

#tato třída slouží k změně hesla uživatele.
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
