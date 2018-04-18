import logging

from django.core.management.base import BaseCommand
from django_mailer import models
from django_mailer.management.commands import create_handler


class Command(BaseCommand):
    help = 'Place deferred messages back in the queue.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-m, --max-retries',
            type='int',
            help="Don't reset deferred messages with more than this many "
                 "retries."
        )

    def handle_noargs(self, verbosity, max_retries=None, **options):
        # Send logged messages to the console.
        logger = logging.getLogger('django_mailer')
        handler = create_handler(verbosity)
        logger.addHandler(handler)

        count = models.QueuedMessage.objects.retry_deferred(
                                                    max_retries=max_retries)
        logger = logging.getLogger('django_mailer.commands.retry_deferred')
        logger.warning("%s deferred message%s placed back in the queue" %
                       (count, count != 1 and 's' or ''))

        logger.removeHandler(handler)
