# Generated by Django 2.0.4 on 2018-12-05 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
    ]