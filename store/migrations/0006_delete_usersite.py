# Generated by Django 3.2 on 2021-04-23 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_merge_0003_usersite_0004_auto_20210419_2117'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSite',
        ),
    ]
