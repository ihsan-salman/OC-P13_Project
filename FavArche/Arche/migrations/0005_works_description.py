# Generated by Django 3.2.4 on 2022-02-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arche', '0004_works_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='description',
            field=models.CharField(default='Description', max_length=500),
        ),
    ]
