# Generated by Django 3.2 on 2021-06-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20210601_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Processing'), (2, 'Intransit'), (3, 'Delivered')], default=1),
        ),
    ]
