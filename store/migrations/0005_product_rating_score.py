# Generated by Django 3.2 on 2021-05-25 12:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_creditcard_exprdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating_score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
