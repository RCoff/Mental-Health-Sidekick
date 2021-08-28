# Generated by Django 3.2.6 on 2021-08-28 07:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('text_app', '0006_auto_20210827_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activesurveystore',
            name='id',
        ),
        migrations.AlterField(
            model_name='activesurveystore',
            name='active_survey_id',
            field=models.UUIDField(default=uuid.UUID('cfeaaf35-e5eb-4921-acc2-2a6d4e07ddba'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='responsemodel',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='text_app.activesurveystore'),
        ),
    ]