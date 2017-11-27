from django.core.management.base import BaseCommand, CommandError
from orf_archive.oe1_download.metadata import retrieve_metadata, update_metadata, get_latest_files
from orf_archive.oe1_download.download import download_file


def update():
    metadata = retrieve_metadata()
    update_metadata(metadata)
    files_to_download = get_latest_files()
    for filename in sorted(files_to_download):
        download_file(filename)



class Command(BaseCommand):
    help = 'Downloads metadata and content, currently Ö1 only'

    def handle(self, *args, **options):
        update()
