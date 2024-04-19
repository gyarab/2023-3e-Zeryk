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
    )
    photo = forms.ImageField(required=False,
                           widget=forms.FileInput(attrs={'class': 'form-control',
                                                         'id': 'photo',
                                                        }))
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'photo']
    
class RecipeSearch(forms.Form):
    ingredients = forms.CharField(label ='Ingridients', max_length=100)