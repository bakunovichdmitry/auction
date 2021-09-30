# Generated by Django 3.1 on 2021-09-30 09:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0003_lot_unique_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='id',
        ),
        migrations.AlterField(
            model_name='lot',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
