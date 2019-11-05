import re

import requests

from find.models import Fasta, MicroRNAAlias

headers = None  # TODO: Implement proper headers


class SequenceNotFoundError(Exception):
    pass


class Uniprot:
    REGEX = r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
    URL = "https://www.uniprot.org/uniprot/{}.fasta"

    @classmethod
    def is_valid(cls, query):
        return bool(re.match(cls.REGEX, query))

    @classmethod
    def get(cls, accession):
        source = cls.URL.format(accession)
        response = requests.get(source, headers=headers)
        if response.status_code == 404:
            raise SequenceNotFoundError("No sequence found in Uniprot: {}".format(accession))
        else:
            content = response.content.decode("utf-8").split("\n")
            description = content[0]
            sequence = "".join(content[1:])
            fasta, _ = Fasta.objects.get_or_create(description=description, sequence=sequence, source=source, accession=accession)
            return fasta


class NCBI:
    REGEX = r'[A-Z]{1,2}_?[0-9]{4,10}\.?[0-9]{1,2}'
    URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={}&id={}&rettype=fasta&retmode=text'

    @classmethod
    def is_valid(cls, query):
        return bool(re.match(cls.REGEX, query))

    @classmethod
    def get(cls, accession):
        source = cls.URL.format('protein', accession)
        response = requests.get(source, headers=headers)
        if response.status_code in [404, 400]:
            source = cls.URL.format('nuccore', accession)
            response = requests.get(source, headers=headers)
            if response.status_code in [404, 400]:
                raise SequenceNotFoundError("No sequence found in Uniprot: {}".format(accession))

        content = response.content.decode("utf-8").split("\n")
        description = content[0]
        sequence = "".join(content[1:])
        fasta, _ = Fasta.objects.get_or_create(description=description, sequence=sequence, source=source, accession=accession)
        return fasta


class Mirbase:
    REGEX = r'MI(MAT)?[0-9]{7}'
    URL = 'http://www.mirbase.org/cgi-bin/get_seq.pl?acc={}'

    @classmethod
    def is_valid(cls, query):
        return bool(re.match(cls.REGEX, query))

    @classmethod
    def get(cls, accession):
        source = cls.URL.format(accession)
        response = requests.get(source, headers=headers)
        content = response.content.decode('utf-8').split('\n')
        if content == '':
            raise SequenceNotFoundError('No sequence found in MirBase: {}'.format(accession))

        description = content[1]
        sequence = content[2]
        fasta, _ = Fasta.objects.get_or_create(description=description, sequence=sequence, source=source, accession=accession)
        return fasta


class MicroRNA:
    REGEX = r'([a-z0-9]{3,7}-(let|mir|miR|bantam|lin|iab|mit|lsy)(-?[a-z0-9]{1,6}(-[0-9]{1,5}l?)?(-(3|5)(p|P))?)?\*?)|bantam'

    @classmethod
    def is_valid(cls, query):
        return bool(re.match(cls.REGEX, query))

    @classmethod
    def get(cls, accession):
        try:
            mirbase_accession = MicroRNAAlias.objects.get(alias=accession.lower()).accession
            return Mirbase.get(mirbase_accession)
        except MicroRNAAlias.DoesNotExist:
            raise SequenceNotFoundError
