# Generated by Django 3.2.4 on 2022-03-01 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0006_delete_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='works',
            name='image',
            field=models.ImageField(null=True, unique=True, upload_to='work_image/'),
        ),
    ]
