# Generated by Django 3.2.4 on 2022-03-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0010_alter_works_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='works',
            name='image',
            field=models.ImageField(blank=True, default='default_work.png', null=True, upload_to='work_image/'),
        ),
    ]
