# Generated by Django 3.2 on 2021-05-26 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rating_order_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='order_item',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.rating'),
        ),
    ]
