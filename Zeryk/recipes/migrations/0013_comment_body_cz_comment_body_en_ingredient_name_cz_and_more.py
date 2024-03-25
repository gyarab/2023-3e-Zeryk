# Generated by Django 5.0.3 on 2024-03-25 14:33

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_alter_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='body_cz',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='body_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='name_cz',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='description_cz',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='description_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='title_cz',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='title_en',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
