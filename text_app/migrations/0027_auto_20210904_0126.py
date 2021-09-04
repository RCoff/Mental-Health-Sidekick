# Generated by Django 3.2.6 on 2021-09-04 05:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('text_app', '0026_alter_activesurveystore_active_survey_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responsemodel',
            old_name='response',
            new_name='mood_response'
        ),
        migrations.AlterField(
            model_name='activesurveystore',
            name='active_survey_id',
            field=models.UUIDField(default=uuid.UUID('f3f6804d-39f4-43c8-895c-08c048a03bf5'), primary_key=True, serialize=False),
        ),
    ]
