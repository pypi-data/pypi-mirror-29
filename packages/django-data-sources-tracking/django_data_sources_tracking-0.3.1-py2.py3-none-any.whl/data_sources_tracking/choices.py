# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


FILE_TYPES = Choices(
    (0, 'tsv', _('tsv')),
    (1, 'csv', _('csv')),
    (2, 'txt', _('txt')),
    (3, 'json', _('json')),
    (4, 'html', _('html')),
    (5, 'fastq', _('fastq')),
    (6, 'bam', _('bam')),
    (7, 'cram', _('cram')),
    (8, 'gvcf', _('gvcf')),
    (9, 'vcf', _('vcf')),
    (10, 'report', _('report')),
    (11, 'bed', _('bed')),
    (12, 'bigwig', _('bigwig')),
    (13, 'wigfix', _('wigfix')),
    (14, 'chromatograms', _('chromatograms')),
    (15, 'other', _('other'))
)
