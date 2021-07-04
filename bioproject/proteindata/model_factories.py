import factory
from django.test import TestCase
from django.conf import settings

from django.utils.crypto import get_random_string
from random import randint

from .models import *


class PfamFactory(factory.django.DjangoModelFactory):
    """Creates Pfam test fixture"""

    domain_id = "PF13041"
    domain_description = "PPRrepeatfamily"

    class Meta:
        model = Pfam

class TaxonomyFactory(factory.django.DjangoModelFactory):
    """Creates Taxonomy test fixture"""

    taxa_id = "180129"
    clade = "O"
    genus = "Oryctolagus Lilljeborg"
    species = "Oryctolagus cuniculus"

    class Meta:
        model = Taxonomy

class ProteinFactory(factory.django.DjangoModelFactory):
    """Creates Protein test fixture"""

    protein_id = get_random_string(length=6)
    sequence = get_random_string(length=20)
    length = randint(10, 1000)
    taxonomy = factory.SubFactory(TaxonomyFactory)

    class Meta:
        model = Protein

class ProteinDomainFactory(factory.django.DjangoModelFactory):
    """Creates ProteinDomain test fixture"""

    protein = factory.SubFactory(ProteinFactory)
    pfam_id = factory.SubFactory(PfamFactory)
    description = "Pentatricopeptide repeat"
    start = randint(1, 100000)
    stop = start+randint(1, 100000)

    class Meta:
        model = ProteinDomain

class ProteinWithDomainFactory(ProteinFactory):
    """Creates Protein with domain test fixture"""

    domain = factory.RelatedFactory(ProteinDomainFactory, 'pfam_id')
