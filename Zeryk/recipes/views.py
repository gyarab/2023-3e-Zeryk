from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from . import models
from .forms import IngredientForm

#TODO cas vareni + filtrovani pomoci casu, likes, comments, id_ingridient (vyhledavani podle ingridienci), hodnoceni receptu(hvezdicky idk??), delete recipe


class RecipeListView(ListView):
  model = models.Recipe
  template_name = 'recipes/home.html'
  context_object_name = 'recipes'

def home(request):
  recipes = models.Recipe.objects.all()
  context = {
    'recipes': recipes
  }
  return render(request, 'recipes/home.html', context)

def about(request):
  return render(request, 'recipes/about.html', {'title': 'about page'})


class RecipeDetailView(DetailView):
  model = models.Recipe

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = models.Recipe
  success_url = reverse_lazy('recipes-home')

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

class RecipeCreateView(LoginRequiredMixin, CreateView):
  model = models.Recipe
  fields = ['title', 'description']

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = models.Recipe
  fields = ['title', 'description']

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

def add_ingredient_to_recipe(request, recipe_id):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            # Предполагается, что у вас есть объект рецепта с идентификатором recipe_id
            recipe = models.Recipe.objects.get(pk=recipe_id)
            recipe.ingredients.add(ingredient)
            return redirect('recipe_detail', pk=recipe_id)  # Замените на ваш URL для просмотра рецепта
    else:
        form = IngredientForm()
    return render(request, 'add_ingredient_to_recipe.html', {'form': form})

