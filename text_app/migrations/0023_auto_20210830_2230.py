# Generated by Django 3.2.6 on 2021-08-31 02:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('text_app', '0022_auto_20210830_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disorder',
            fields=[
                ('disorder', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('disorder_shortname', models.CharField(blank=True, max_length=10, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='activesurveystore',
            name='active_survey_id',
            field=models.UUIDField(default=uuid.UUID('ca110a8d-9ca9-44ed-ba71-4230a2845b27'), primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='dailysymptoms',
            name='disorder',
            field=models.ManyToManyField(to='text_app.Disorder'),
        ),
    ]