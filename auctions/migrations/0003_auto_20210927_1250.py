# Generated by Django 3.1 on 2021-09-27 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210927_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='option',
            field=models.IntegerField(choices=[(0, 'DUTCH'), (1, 'ENGLISH')]),
        ),
    ]
