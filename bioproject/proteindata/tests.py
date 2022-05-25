import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# Create your tests here.

class ProteinSerializerTest(APITestCase):
    protein1 = None
    proteinSerializer = None

    def setUp(self):
        self.protein1 = ProteinFactory.create(pk=1, protein_id="A0A014PQC0")
        self.proteinSerializer = ProteinSerializer(instance=self.protein1)
        self.domain1 = PfamFactory.create()
        self.protein_domain1 = ProteinDomainFactory.create(protein=self.protein1, pfam_id=self.domain1)

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

    def test_proteinSerializerHasAllKeys(self):
        """
        Ensure that all keys in the object are included in the serializer
        """
        data = self.proteinSerializer.data
        self.assertEqual(set(data.keys()), set(['protein_id', 'sequence', 'length', 'taxonomy', 'domains']))


class GetProteinTest(APITestCase):
    """
    Test module for protein GET request
    """

    protein1 = None
    good_url = ''
    bad_url = ''
    delete_url = ''

    def setUp(self):
        # Create proteins
        self.protein1 = ProteinFactory.create(pk=1, protein_id='A0A014PQC0')
        self.domain1 = PfamFactory.create()
        self.protein_domain1 = ProteinDomainFactory.create(protein=self.protein1, pfam_id=self.domain1)

        # Set urls
        self.good_url = reverse('protein_api', kwargs={'protein_id': 'A0A014PQC0'})
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
        Ensure we get an 200 OK status code when making a valid GET request.
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
        Ensure we get the domain id data of the requested protein
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertTrue('PF13041' in data['domains'][0]['pfam_id']['domain_id'])

    def test_proteinDetailReturnFailOnBadProteinId(self):
        """
        Ensure we get a 404 Bad status code when making a get request with an invalid id
        """
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)


class PostProteinTest(APITestCase):
    """
    Test module for protein POST request
    """

    valid_protein = ''
    invalid_protein = ''
    good_url = ''
    bad_url = ''

    def setUp(self):
        # Add taxonomy, factory data
        TaxonomyFactory.create()
        PfamFactory.create()

        # Set valid and invalid data
        self.valid_protein = {
            "protein_id": "Z0Z1000",
            "sequence": "MVIGVGFLLVLFSSSVLGILNAGVQLRI",
            "taxonomy": {
                "taxa_id": 180129,
                "clade": "O",
                "genus": "Oryctolagus Lilljeborg",
                "species": "Oryctolagus cuniculus"
            },
            "length": 101,
            "domains": [
                {
                    "pfam_id": {
                        "domain_id": "PF13041",
                        "domain_description": "PPRrepeatfamily"
                    },
                    "description": "PPRrepeatfamily",
                    "start": 40,
                    "stop": 94
                }
            ]
        }

        self.invalid_protein = {
            "protein_id": "",
            "sequence": "MVIGVGFLLVLFSSSVLGILNAGVQLRI",
            "taxonomy": {
                "taxa_id": 180129,
                "clade": "O",
                "genus": "Oryctolagus Lilljeborg",
                "species": "Oryctolagus cuniculus"
            },
            "length": 101,
            "domains": [
                {
                    "pfam_id": {
                        "domain_id": "PF13041",
                        "domain_description": "PPRrepeatfamily"
                    },
                    "description": "PPRrepeatfamily",
                    "start": 40,
                    "stop": 94
                }
            ]
        }

        # Set urls
        self.good_url = reverse('create_protein_api')

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


    def test_createValidProtein(self):
        """
        Ensure we are able to create a new protein with a POST request
        """

        response = self.client.post(self.good_url, self.valid_protein, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Protein.objects.get(protein_id='Z0Z1000').protein_id, 'Z0Z1000')

    def test_createInvalidProtein(self):
        """
        Ensure that POST requests with invalid data fails
        """

        response = self.client.post(self.good_url, self.invalid_protein, format='json')
        self.assertEqual(response.status_code, 400)


class GetPfamTest(APITestCase):
    """
    Test module for pfam GET request
    """

    pfam = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        # Create pfam
        self.pfam = PfamFactory.create()

        # Set urls
        self.good_url = reverse('pfam_api', kwargs={'domain_id': 'PF13041'})
        self.bad_url = '/api/pfam/H/'

    def tearDown(self):

        # Reset test tables
        Pfam.objects.all().delete()

        # Reset primary keys
        PfamFactory.reset_sequence(0)

    def test_pfamReturnSuccess(self):
        """
        Ensure we get an 200 OK status code when making a valid GET request.
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_PfamReturnCorrectDomainId(self):
        """
        Ensure we get the domain id of the requested pfam
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertIn(data['domain_id'], 'PF13041')

    def test_PfamReturnCorrectDomainDescription(self):
        """
        Ensure we get the domain id of the requested pfam
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertIn(data['domain_description'], 'PPRrepeatfamily')

    def test_PfamReturnFailOnBadPfam(self):
        """
        Ensure we get a 404 Bad status code when making a get request with an invalid id
        """
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)


class GetCoverage(APITestCase):
    """
    Test module for coverage GET request
    """

    protein = None
    domain = None
    protein_domain = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        # Create protein with domain with the same start, stop and length as the real A0A014PQC0
        self.protein = ProteinFactory.create(pk=1, protein_id='A0A014PQC0', length=338)
        self.domain = PfamFactory.create()
        self.protein_domain = ProteinDomainFactory.create(protein=self.protein, 
                                                            pfam_id=self.domain, 
                                                            start=157, 
                                                            stop=314)

        # Set urls
        self.good_url = reverse('protein_coverage', kwargs={'protein_id': 'A0A014PQC0'})

    def tearDown(self):

        # Reset test tables
        Protein.objects.all().delete()
        Pfam.objects.all().delete()
        ProteinDomain.objects.all().delete()

        # Reset primary keys
        ProteinFactory.reset_sequence(0)
        PfamFactory.reset_sequence(0)
        ProteinDomainFactory.reset_sequence(0)

    def test_coverageReturnSuccess(self):
        """
        Ensure we get an 200 OK status code when making a valid GET request.
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_coverageReturnCorrectCoverage(self):
        """
        Ensure we get the right coverage of the requested protein
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertEqual(data, 0.46449704142011833)
