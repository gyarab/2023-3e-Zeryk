from modeltranslation.translator import register, TranslationOptions
from .models import Ingredient, Recipe, Comment

@register(Ingredient)
class IngredientTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('body',)