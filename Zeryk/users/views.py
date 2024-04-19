from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from recipes.models import Recipe
from .models import UserProfile
from . import forms

#TODO dodelat kolik liku mas celkem, profilovka, recepty ktery jsem likenul, (pod profilovkou by se dalo udelat kolik hvezdicek z 5 ma, podle toho jak hodnotili tvuj recept, asi nejakym aritmetickym prumerem)

def register(request):
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST, request.FILES)
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
        form = forms.UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout(request):
  logout(request)
  return redirect('user-login')

@login_required()
def profile(request):
  user = request.user
  recipes = Recipe.objects.filter(author=user)
  return render(request, 'users/profile.html', {'recipes': recipes})

