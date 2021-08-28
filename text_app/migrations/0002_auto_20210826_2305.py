# Generated by Django 3.2.6 on 2021-08-27 03:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('text_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsemodel',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e3ce314c-39c0-4034-a730-514a9c3756cd'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='responsemodel',
            name='response',
            field=models.CharField(choices=[(1, 1), (2, 2)], max_length=1),
        ),
    ]