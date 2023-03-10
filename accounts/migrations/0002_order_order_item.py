# Generated by Django 3.2.12 on 2023-01-28 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('isPaid', models.BooleanField(default=False)),
                ('provider_order_id', models.CharField(max_length=40)),
                ('payment_id', models.CharField(max_length=36)),
                ('signature_id', models.CharField(max_length=128)),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('mode', models.CharField(choices=[('Online', 'ONLINE'), ('Offline', 'OFFLINE'), ('ASSISTED', 'ASSISTED')], default='ASSISTED', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.FloatField()),
                ('provider_order_id', models.CharField(max_length=40)),
                ('item_qty', models.IntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
