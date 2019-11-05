import os
from urllib.request import urlopen
from zipfile import ZipFile
import io

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'FastaFinder.settings'
django.setup()

from find.models import MicroRNAAlias
from find.sources import MicroRNA


def update_microrna_aliases():
    mysock = urlopen('ftp://mirbase.org/pub/mirbase/CURRENT/aliases.txt.zip')

    memfile = io.BytesIO(mysock.read())
    with ZipFile(memfile, 'r') as myzip:
        f = myzip.open('aliases.txt')
        content = f.read()
        lines = [line.split('\t') for line in content.decode('utf-8').split('\n') if line != '']

    mapping = {}
    for line in lines:
        micrornas = [mir.lower() for mir in line[1].split(';') if mir != '']
        accession = line[0]
        for mir in micrornas:
            mapping[mir] = accession

    MicroRNAAlias.objects.all().delete()
    for alias, accession in mapping.items():
        MicroRNAAlias.objects.create(alias=alias, accession=accession)


if __name__ == '__main__':
    update_microrna_aliases()