from django import forms
from .models import Ingredient, Comment, Recipe
from django.utils.safestring import mark_safe

#formulář pro ingredience
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']

#definuje formulář pro vytváření a úpravu instancí modelu Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            #'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class IngredientCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        final_attrs = self.get_context(name, value, attrs)['widget']['attrs']
        output = [mark_safe('<div class="column">')]
        str_values = {str(v) for v in value}  # Normalize to strings.
        for i, (option_value, option_label) in enumerate(self.choices):
            if i % 10 == 0 and i != 0:
                output.append(mark_safe('</div><div class="column">'))
            id_ = final_attrs.get('id') + '_{}'.format(i)  # Construct id for each checkbox
            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            rendered_cb = cb.render(name, option_value)
            output.append('<label for="{}">{}</label>'.format(id_, rendered_cb + ' ' + option_label))
        output.append(mark_safe('</div>'))
        return mark_safe('\n'.join(output))


class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=IngredientCheckboxSelectMultiple,
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'photo'}),
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'photo']

    
#umožňuje uživateli zadat textový řetězec (seznam ingrediencí) a použít ho pro vyhledávání receptů.
class RecipeSearch(forms.Form):
    ingredients = forms.CharField(label ='Ingridients', max_length=100)