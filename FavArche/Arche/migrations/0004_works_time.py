# Generated by Django 3.2.4 on 2022-02-16 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('arche', '0003_alter_works_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
