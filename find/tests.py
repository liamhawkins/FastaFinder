from django.test import TestCase

# Create your tests here.
from find.sources import Uniprot, NCBI, Mirbase, MicroRNA
from find.views import sources


class SourceRegexTestCase(TestCase):
    accessions = {
        Uniprot: ['P60709', 'P04797', 'Q28554', 'Q5RAB4', 'B7ZS96', 'A0A1L8GTR7'],
        NCBI: ['NP_002037.2', 'NP_001344872.1', 'NP_001344872', 'NM_001115114.1', 'NC_000012.12'],
        Mirbase: ['MI0041063', 'MI0006244', 'MI0000060', 'MIMAT0000062', 'MIMAT0050475'],
        MicroRNA: ['smc-miR-12455-5p', 'smc-mir-12455-1', 'ddi-mir-1176', 'hsa-let-7a-1', 'hsa-let-7a-5p'],
    }

    def test(self):
        for source, accessions in self.accessions.items():
            other_sources = [s for s in sources if s != source]
            for accession in accessions:
                self.assertTrue(source.is_valid(accession))

                for other_source in other_sources:
                    self.assertFalse(other_source.is_valid(accession))