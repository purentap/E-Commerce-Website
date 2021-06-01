# Generated by Django 3.2 on 2021-05-26 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='rating_score',
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]