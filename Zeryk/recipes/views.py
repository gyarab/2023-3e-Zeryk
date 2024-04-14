from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from . import models
from .forms import RecipeForm, CommentForm, RecipeSearch
import requests
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse


#TODO delete comment, cas vareni + filtrovani pomoci casu


def like(request, pk):
  post = get_object_or_404(models.Recipe, id=request.POST.get('object_id'))
  liked = False
  if post.likes.filter(id=request.user.id).exists():
      post.likes.remove(request.user)
      liked = False
  else:
      post.likes.add(request.user)
      liked = True

  return HttpResponseRedirect(reverse('recipes-detail', args=[str(pk)]))

def home(request):
  recipes = models.Recipe.objects.all().order_by('-created_at')
  context = {
    'recipes': recipes
  }
  return render(request, 'recipes/home.html', context)

def about(request):
  return render(request, 'recipes/about.html', {'title': 'about page'})

def search_ingredients(request):
    query = request.GET.get('query')
    if query:
        results = models.Ingredient.objects.filter(name__icontains=query)
        data = [{'id': result.id, 'name': result.name} for result in results]
        return JsonResponse({'results': data})
    else:
        return JsonResponse({'results': []})

def search_recipes(request):
  form = RecipeSearch(request.GET)
  if form.is_valid():
      ingredients = form.cleaned_data['ingredients']
      recipes = models.Recipe.objects.filter(
          ingredients__name__in=ingredients.split(',')
      )
      return render(request, 'recipes/search.html', {'recipes': recipes})
  else:
      form = RecipeSearch()
  return render(request, 'home.html', {'form': form})

class RecipeListView(ListView):
  model = models.Recipe
  template_name = 'recipes/home.html'
  context_object_name = 'recipes'

class RecipeDetailView(DetailView):
  model = models.Recipe
  template_name = 'recipes/recipe_detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(RecipeDetailView, self).get_context_data(*args, **kwargs)

    stuff = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
    total_likes = stuff.total_likes()

    liked = False
    if stuff.likes.filter(id=self.request.user.id).exists():
        liked = True

    context["total_likes"] = total_likes
    context["liked"] = liked
    return context

class AddCommentView(CreateView):
    model = models.Comment
    form_class = CommentForm
    template_name = 'recipes/add_comment.html'
    
    def form_valid(self, form):
        form.instance.post = models.Recipe.objects.get(pk=self.kwargs.get("pk"))
        form.instance.name = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('recipes-home')

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = models.Recipe
  success_url = reverse_lazy('recipes-home')

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
  
class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'description','ingredients']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.ingredients.all()
        return context

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def unknown(request, exception):
    return render(request, 'recipes/404.html', status=404)