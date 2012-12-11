from django.core.management.base import BaseCommand, CommandError
from cyder.dnsutils.network_build import migrate_networks


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        migrate_networks()
