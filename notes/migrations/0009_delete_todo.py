# Generated by Django 5.0.6 on 2024-11-22 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_todo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Todo',
        ),
    ]