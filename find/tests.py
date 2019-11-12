from django.test import TestCase

# Create your tests here.
from find.sources import Uniprot, NCBI, Mirbase, MicroRNA
from find.views import sources, is_genome


class SourceIsValidTestCase(TestCase):
    accessions = {
        Uniprot: ['P60709', 'P04797', 'Q28554', 'Q5RAB4', 'B7ZS96', 'A0A1L8GTR7'],
        NCBI: ['NP_002037.2', 'NP_001344872.1', 'NP_001344872', 'NM_001115114.1', 'NC_000012.12'],
        Mirbase: ['MI0041063', 'MI0006244', 'MI0000060', 'MIMAT0000062', 'MIMAT0050475'],
        MicroRNA: ['smc-miR-12455-5p', 'smc-mir-12455-1', 'ddi-mir-1176', 'hsa-let-7a-1', 'hsa-let-7a-5p'],
    }

    bad_accessions = ['this_is_not_a_protein', '123123123', 'nc.cnd.sjfdkal', 'weeeeewooooweeeewooooo', '1=1 OR \'']

    def test_real_accessions(self):
        for source, accessions in self.accessions.items():
            other_sources = [s for s in sources if s != source]
            for accession in accessions:
                self.assertTrue(source.is_valid(accession))

                for other_source in other_sources:
                    self.assertFalse(other_source.is_valid(accession))

    def test_bad_accessions(self):
        for accession in self.bad_accessions:
            for source in sources:
                self.assertFalse(source.is_valid(accession))


class ViewsTestCase(TestCase):
    def test_is_genome(self):
        genomes = ['NC_000012.12']
        not_genomes = ['P60709']

        for g in genomes:
            self.assertTrue(is_genome(g))

        for ng in not_genomes:
            self.assertFalse(is_genome(ng))