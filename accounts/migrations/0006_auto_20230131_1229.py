# Generated by Django 3.2.12 on 2023-01-31 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20230131_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ORDER_STATUS',
            field=models.CharField(choices=[('IN_PROGRESS', 'IN_PROGRESS'), ('CANCELLED', 'CANCELLED'), ('SHIPPED', 'SHIPPED'), ('ACCEPTED', 'ACCEPTED'), ('NOT_CREATED', 'NOT_CREATED'), ('CREATED', 'CREATED')], default='NOT_CREATED', max_length=15),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='ORDER_STATUS',
            field=models.CharField(choices=[('IN_PROGRESS', 'IN_PROGRESS'), ('CANCELLED', 'CANCELLED'), ('SHIPPED', 'SHIPPED'), ('ACCEPTED', 'ACCEPTED'), ('NOT_CREATED', 'NOT_CREATED'), ('CREATED', 'CREATED')], default='NOT_CREATED', max_length=15),
        ),
    ]