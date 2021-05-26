# Generated by Django 3.2 on 2021-05-26 15:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20210526_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
