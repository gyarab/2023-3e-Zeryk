# Generated by Django 5.0.3 on 2024-03-15 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
    ]
