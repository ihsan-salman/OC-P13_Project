# Generated by Django 3.2.4 on 2022-03-15 10:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='users',
            field=models.ManyToManyField(help_text='user who are connected to the chat', to=settings.AUTH_USER_MODEL),
        ),
    ]