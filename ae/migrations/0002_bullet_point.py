# Generated by Django 3.2.12 on 2023-01-28 07:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ae', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bullet_point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(max_length=60)),
                ('modified_at', models.DateTimeField(default=datetime.datetime.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ae.product')),
            ],
        ),
    ]