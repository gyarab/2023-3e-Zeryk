from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


#definuje jednoduchou entitu ingredience s jedním polem name, které reprezentuje název ingredience.
class Ingredient(models.Model):
  name = models.CharField(max_length=100)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name

#definuje databázovou tabulku pro uchovávání informací o receptech v aplikaci. 
class Recipe(models.Model):
  title = models.CharField(max_length=100, verbose_name=_('title'))
  description = RichTextField(blank=True, null=True, verbose_name=_('description'), config_name='default')
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  ingredients = models.ManyToManyField(Ingredient, related_name='recipes', verbose_name=_('ingredients'))
  likes = models.ManyToManyField(User, related_name='blog_posts')
  photo = models.ImageField(
        upload_to='recipes',
        null=True,
        blank=True,
        verbose_name=_('photo'),
    )

  class Meta:
    ordering = ['-created_at']

  def get_absolute_url(self):
    return reverse("recipes-detail", kwargs={"pk": self.pk})
  
  def total_likes(self):
    return self.likes.count()

  def __str__(self):
    return self.title
  
#reprezentuje komentář k receptu.
class Comment(models.Model):
  post = models.ForeignKey(Recipe, related_name="comments", on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  body = RichTextField(blank=True, null=True)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return '%s - %s' % (self.post.title, self.name)

