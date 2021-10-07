# Generated by Django 3.1 on 2021-09-30 09:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0002_auto_20210929_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
