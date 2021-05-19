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

    pfam_id = PfamSerializer(many=False, read_only=True)

    class Meta:
        model = ProteinDomain
        fields = ['pfam_id', 'description', 'start', 'stop']

class ProteinSerializer(serializers.ModelSerializer):

    domains = ProteinDomainSerializer(source="domain_to_protein", many=True)
    taxonomy = TaxonomySerializer(many=False)

    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']

class ProteinListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Protein
        fields = ['id', 'protein_id']

