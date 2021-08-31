from django.core.management.base import BaseCommand
import datetime
from text_app.models import Disorder


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        disorder_list = (
            ('Bipolar', 'BPD'),
            ('Attention-deficit/hyperactivity disorder', 'ADHD'),
        )

        for disorder in disorder_list:
            add_disorder, created = Disorder.objects.get_or_create(
                disorder=disorder[0],
                disorder_shortname=disorder[1]
            )
