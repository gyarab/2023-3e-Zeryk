# Generated by Django 5.0.3 on 2024-03-15 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_remove_comment_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created_on',
            new_name='date_added',
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]