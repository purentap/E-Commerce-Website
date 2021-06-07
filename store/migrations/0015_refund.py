# Generated by Django 3.2 on 2021-06-05 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval', models.IntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Disapproved')], default=1)),
                ('onDiscount', models.BooleanField(default=False)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('order_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.orderitem')),
            ],
        ),
    ]