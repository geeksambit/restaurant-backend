# Generated by Django 2.0.4 on 2019-02-12 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_deliveryboy_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fcm_id',
            field=models.CharField(blank=True, default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='vendor',
            name='fcm_id',
            field=models.CharField(blank=True, default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='deliveryboy',
            name='route',
            field=models.CharField(blank=True, default=None, max_length=200),
        ),
    ]
