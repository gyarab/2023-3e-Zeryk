from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from . import models
from .forms import IngredientForm, CommentForm

#TODO cas vareni + filtrovani pomoci casu, likes, comments, id_ingridient (vyhledavani podle ingridienci), hodnoceni receptu(hvezdicky idk??), delete recipe


def LikeView(request, pk):
  post = get_object_or_404(models.Recipe, id=request.POST.get('post_id'))
  liked = False
  if post.likes.filter(id=request.user.id).exists():
      post.likes.remove(request.user)
      liked = False
  else:
      post.likes.add(request.user)
      liked = True

  return HttpResponseRedirect(reverse('recipe-detail', args=[str(pk)]))

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
    template_name = 'add_comment.html'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('home')

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

