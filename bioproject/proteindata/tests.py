import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# Create your tests here.

class ProteinTest(APITestCase):

    protein1 = None
    protein2 = None
    protein3 = None
    good_url = ''
    bad_url = ''
    delete_url = ''

    def setUp(self):
        # Create proteins
        self.protein1 = ProteinFactory.create(pk=1, protein_id="A0A014PQC0")
        self.domain1 = PfamFactory.create()
        self.protein_domain1 = ProteinDomainFactory.create(protein=self.protein1, pfam_id=self.domain1)

        # Set urls
        self.good_url = reverse("protein_api", kwargs={"protein_id": "A0A014PQC0"})
        self.bad_url = '/api/protein/H/'

    def tearDown(self):

        # Reset test tables
        Pfam.objects.all().delete()
        Taxonomy.objects.all().delete()
        ProteinDomain.objects.all().delete()
        Protein.objects.all().delete()

        # Reset primary keys
        PfamFactory.reset_sequence(0)
        TaxonomyFactory.reset_sequence(0)
        ProteinDomainFactory.reset_sequence(0)
        ProteinFactory.reset_sequence(0)


    def test_proteinDetailReturnSuccess(self):
        """
        Ensure we get an 200 OK status code when making a valid get request.
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_proteinDetailReturnCorrectTaxaId(self):
        """
        Ensure we get the taxonomy id of the requested protein
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertIn(data['taxonomy']['taxa_id'], '180129')

    def test_proteinDetailContainPfamId(self):
        """
        Ensure we get the domain data of the requested protein
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertTrue('pfam_id' in data['domains'][0])

    def test_proteinDetailReturnFailOnBadProteinId(self):
        """
        Ensure we get a 404 Bad status code when making a get request with an invalid id
        """
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

