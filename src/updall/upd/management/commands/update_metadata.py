from django.core.management.base import BaseCommand, CommandError
from prettytable import PrettyTable

from upd.models import Product


class Command(BaseCommand):
    help = 'update fw metadata'

    def handle(self, *args, **options):
        from upd.lib import UpdateAllTheThings
        upd = UpdateAllTheThings()
        upd.update_metadata()
        all_latest = upd.get_all_latest()

        table = PrettyTable(align='l')
        table.field_names = ['Product', 'Latest Version', 'Date Published']
        table.align = 'l'

        for latest in all_latest:
            table.add_row([latest.product.name, latest.version, latest.date_published])

        print(table)
        self.stdout.write(self.style.SUCCESS('Successfully updated fw metadata'))