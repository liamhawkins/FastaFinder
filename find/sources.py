import re
from collections import namedtuple

import requests

headers = None  # TODO: Implement proper headers


class SequenceNotFoundError(Exception):
    pass


FastaSeq = namedtuple("Fasta", ["description", "sequence", "source", "accession"])


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
            return FastaSeq(
                description=description,
                sequence=sequence,
                source=source,
                accession=accession,
            )


if __name__ == "__main__":
    query = "B7NR61"
    if Uniprot.is_valid(query):
        fs = Uniprot.get(query)
        print("test")
