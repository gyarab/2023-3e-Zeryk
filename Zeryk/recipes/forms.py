from django import forms
from .models import Ingredient, Comment, Recipe

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            #'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class RecipeForm(forms.ModelForm):
    search_ingredient = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'placeholder': 'Search ingredients...', 'class': 'form-control'}))

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_ingredient'].widget.attrs['id'] = 'search-ingredient'

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.author = self.request.user
            recipe.save()
            for ingredient in self.cleaned_data['ingredients']:
                recipe.ingredients.add(ingredient)
        return recipe
    
class RecipeSearch(forms.Form):
    ingredients = forms.CharField(label ='Ingridients', max_length=100)