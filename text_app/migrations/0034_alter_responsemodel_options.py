# Generated by Django 3.2.6 on 2021-09-07 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_app', '0033_alter_activesurveystore_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='responsemodel',
            options={'ordering': ['created_datetime']},
        ),
    ]
