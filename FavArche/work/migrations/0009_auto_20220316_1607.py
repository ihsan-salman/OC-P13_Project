# Generated by Django 3.2.4 on 2022-03-16 15:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work', '0008_alter_works_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='fav',
            field=models.ManyToManyField(blank=True, default=None, related_name='work_post_fav', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='works',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='work_post_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
