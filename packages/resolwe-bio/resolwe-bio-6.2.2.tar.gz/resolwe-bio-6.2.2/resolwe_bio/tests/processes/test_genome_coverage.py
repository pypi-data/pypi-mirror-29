# pylint: disable=missing-docstring
from resolwe.test import tag_process
from resolwe_bio.utils.test import BioProcessTestCase


class CoverageProcessorTestCase(BioProcessTestCase):

    @tag_process('bam-coverage')
    def test_coverage(self):
        with self.preparation_stage():
            genome = self.prepare_genome()
            reads = self.prepare_reads()

            inputs = {'src': 'annotation.gff.gz', 'source': 'DICTYBASE'}
            annotation = self.run_process('upload-gff3', inputs)

            inputs = {
                'genome': genome.pk,
                'reads': reads.pk,
                'gff': annotation.pk,
                'PE_options': {
                    'library_type': "fr-unstranded"}}
            aligned_reads = self.run_process('alignment-tophat2', inputs)

        inputs = {'bam': aligned_reads.pk}

        coverage = self.run_process('bam-coverage', inputs)
        self.assertFile(coverage, 'bigwig', 'genome_coverage.bw')
