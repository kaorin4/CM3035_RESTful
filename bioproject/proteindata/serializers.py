from rest_framework import serializers
from .models import *

class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ['domain_id', 'domain_description']

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']

class ProteinDomainSerializer(serializers.ModelSerializer):

    domain = PfamSerializer(many=False, read_only=True)

    class Meta:
        model = ProteinDomain
        fields = ['domain', 'start', 'stop']

class ProteinSerializer(serializers.ModelSerializer):

    domains = ProteinDomainSerializer(source="domain_to_protein", many=True, read_only=True)
    taxonomy = TaxonomySerializer(many=False, read_only=True)

    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']

class ProteinByTaxonomySerializer(serializers.ModelSerializer):

    class Meta:
        model = Protein
        fields = ['id', 'protein_id']

