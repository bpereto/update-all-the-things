from django.core.management.base import BaseCommand
from upd.lib import UpdateAllTheThings


class Command(BaseCommand):
    """
    download latest fw
    """
    help = 'download latest fw of all products'

    def handle(self, *args, **options):
        upd = UpdateAllTheThings()
        all_latest = upd.get_all_latest()
        for version in all_latest:
            try:
                self.stdout.write(f'download {version}')
                upd.download_fw_version(version)
            except AssertionError:
                print(str(version) + ' already downloaded.')

        self.stdout.write(self.style.SUCCESS('Successfully downloaded latest fw'))
