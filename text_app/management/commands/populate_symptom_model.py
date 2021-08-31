from django.core.management.base import BaseCommand, CommandError
import datetime
import uuid
from text_app.models import Disorder, DailySymptoms


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        disorder_list = (
            ('Bipolar', 'BPD'),
            ('Attention-deficit/hyperactivity disorder', 'ADHD'),
        )

        symptom_list = ['irritable', 'reckless spending', 'less sleep', 'racing thoughts', 'distractable',
                        'goal-driven', 'fidgety', 'good mood', 'unmotivated', 'indecisive', 'shame', 'hopeless',
                        'sedentary', 'low hygiene', 'media binge', 'more sleep']

        bpd_obj = Disorder.objects.get(disorder='Bipolar')
        adhd_obj = Disorder.objects.get(disorder='Attention-deficit/hyperactivity disorder')

        for symptom in symptom_list:
            add_symptom, created = DailySymptoms.objects.get_or_create(
                symptom=symptom
            )
            add_symptom.disorder.add(adhd_obj)
            add_symptom.disorder.add(bpd_obj)
            add_symptom.save()
