# Generated by Django 2.0.4 on 2018-12-13 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_vendor_image'),
        ('orders', '0007_order_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.Vendor'),
            preserve_default=False,
        ),
    ]