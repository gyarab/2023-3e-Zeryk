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
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients']

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.author = self.request.user
            recipe.save()
            for ingredient in self.cleaned_data['ingredients']:
                recipe.ingredients.add(ingredient)
        return recipe