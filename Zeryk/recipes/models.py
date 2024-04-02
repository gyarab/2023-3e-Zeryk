from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 

#TODO dodelat pridat ingridients, pole, vytvareni pole, databaze, nejak spojit

class Ingredient(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Recipe(models.Model):
  title = models.CharField(max_length=100)
  description = RichTextField(blank=True, null=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  ingredients = models.ManyToManyField(Ingredient)
  likes = models.ManyToManyField(User, related_name='blog_posts')

  class Meta:
    ordering = ['-created_at']

  def get_absolute_url(self):
    return reverse("recipes-detail", kwargs={"pk": self.pk})
  
  def total_likes(self):
    return self.likes.count()

  def __str__(self):
    return self.title
  
class Comment(models.Model):
  post = models.ForeignKey(Recipe, related_name="comments", on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  body = RichTextField(blank=True, null=True)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return '%s - %s' % (self.post.title, self.name)

