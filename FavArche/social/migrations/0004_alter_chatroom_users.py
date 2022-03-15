# Generated by Django 3.2.4 on 2022-03-15 12:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0003_alter_chatroom_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
