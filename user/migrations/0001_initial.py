# Generated by Django 2.0.4 on 2018-10-08 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryBoy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('mobile_no', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('reset_password', models.CharField(default=0, max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=200)),
                ('route', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAdress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('mobile_no', models.CharField(max_length=200)),
                ('pin', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('landmark', models.CharField(default=None, max_length=200)),
                ('longitude', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('mobile_no', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('salt', models.CharField(blank=True, max_length=200)),
                ('jwt_token', models.CharField(blank=True, max_length=500)),
                ('reset_password', models.CharField(default=0, max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('social_id', models.CharField(blank=True, max_length=200)),
                # ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('mobile_no', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                # ('salt', models.CharField(blank=True, max_length=200)),
                # ('jwt_token', models.CharField(blank=True, max_length=500)),
                # ('reset_password', models.CharField(default=0, max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                # ('updated_date', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=200)),
                ('longitude', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='shippingadress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]