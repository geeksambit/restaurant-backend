# Generated by Django 2.0.4 on 2018-12-05 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='image',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
