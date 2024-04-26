from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from recipes.models import Recipe
from .models import UserProfile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.utils.translation import gettext_lazy as _

#funkce register, která zpracovává požadavky na registraci nových uživatelů. Přijímá požadavky metodou POST, když je formulář odeslán, a metodou GET, když se poprvé zobrazuje stránka pro registraci.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            profile = UserProfile.objects.get(user=user)
            profile.pfp = form.cleaned_data.get('pfp')
            profile.save()
            messages.success(request, f"{username}, your account is created, please login.")
            return redirect('user-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

#tato funkce zobrazuje profil uživatele a zobrazuje seznam receptů, které uživatel vytvořil. @login_required znamená, že je přístupný pouze přihlášeným uživatelům.
@login_required
def profile(request):
    user = request.user
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'users/profile.html', {'recipes': recipes})

#tato funkce je určena k zobrazení seznamu receptů, které daný uživatel označil jako oblíbené.
@login_required
def liked_recipes(request):
    liked_recipes = Recipe.objects.filter(likes=request.user)
    return render(request, 'users/liked_recipes.html', {'liked_recipes': liked_recipes})

#funkce umožňuje uživatelům aktualizovat své účetní informace.
@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your account has been updated!'))
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    return render(request, 'users/settings.html', {'user_form': user_form, 'profile_form': profile_form})

#funkce umožňuje uživatelům změnit své heslo. 
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('user-profile')
        else:
            messages.error(request, _('Error updating your password.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})
