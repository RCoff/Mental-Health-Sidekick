# Generated by Django 3.2.6 on 2021-08-28 17:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('text_app', '0014_alter_activesurveystore_active_survey_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activesurveystore',
            name='active_survey_id',
            field=models.UUIDField(default=uuid.UUID('4fdc46b0-78fd-4927-868c-6a33c70403ac'), primary_key=True, serialize=False),
        ),
    ]
