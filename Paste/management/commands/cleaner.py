import sys

from django.core.management.base import BaseCommand
from django.utils import timezone

from Paste.models import Paste


class Command(BaseCommand):
    """
    Usage: 30 * * * * python3 /home/mertcan/yapistir_io/manage.py cleaner > /dev/null
    """

    help = "Suresi Gecen Icerikleri Sil"

    def handle(self, *args, **options):
        deleteable_pastes = Paste.objects.filter(
            expire__isnull=False,
            expire__lte=timezone.now()
        )
        sys.stdout.write(u"Toplam Silinen Icerik Sayisi: %s \n" % deleteable_pastes.count())
        for d in deleteable_pastes:
            sys.stdout.write(u"- %s (%s)\n" % (d.slug, d.expire))
            deleteable_pastes.update(is_removed=True)
