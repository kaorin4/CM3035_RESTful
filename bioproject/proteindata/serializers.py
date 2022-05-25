from rest_framework import serializers
from .models import *

class PfamSerializer(serializers.ModelSerializer):
    """
    Pfam Serializer that includes domain_id and domain_description fields
    """

    domain_id = serializers.CharField(required=True)
    domain_description = serializers.CharField(required=False)

    class Meta:
        model = Pfam
        fields = ['domain_id', 'domain_description']


class TaxonomySerializer(serializers.ModelSerializer):

    taxa_id = serializers.RegexField(regex=r'^[0-9]+$', required=True)
    clade = serializers.CharField(required=False)
    genus = serializers.CharField(required=False)
    species = serializers.CharField(required=False)

    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']


class ProteinDomainSerializer(serializers.ModelSerializer):

    pfam_id = PfamSerializer(many=False)
    start = serializers.IntegerField(required=True)
    stop = serializers.IntegerField(required=True)

    class Meta:
        model = ProteinDomain
        fields = ['pfam_id', 'description', 'start', 'stop']

    def validate(self, data):
        """
        Check that the start is before stop
        """
        if data['start'] > data['stop']:
            raise serializers.ValidationError('Stop should be greater than start')
        return data

    def create(self, validated_data):
        protein = validated_data.get('protein')
        domain = self.initial_data.get('pfam_id')

        protein_domain = ProteinDomain(**{**validated_data,
                            'protein': Protein.objects.get(protein_id=protein['protein_id']),
                            'pfam_id': Pfam.objects.get(domain_id=domain['pfam_id'])
                        })
        protein_domain.save()


class ProteinSerializer(serializers.ModelSerializer):

    domains = ProteinDomainSerializer(source="domains_in_protein", many=True)
    taxonomy = TaxonomySerializer(many=False)
    sequence = serializers.CharField(required=True)
    length = serializers.IntegerField(required=True)

    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']

    def validate_length(self, length):
        """
        Check that the length is a positive number
        """
        if length < 1:
            raise serializers.ValidationError("Length should be positive")
        return length

    def create(self, validated_data):
        taxonomy_data = validated_data.pop('taxonomy')
        protein_domains_data = validated_data.pop('domains_in_protein')
        domains = self.initial_data.get('domains')

        # create new protein and pass data as Python Dict
        protein = Protein(**{**validated_data,
                        'taxonomy': Taxonomy.objects.get(taxa_id=taxonomy_data['taxa_id'])
                        })
        protein.save()

        # for each domain, create a protein_domain
        for domain in domains:
            pfam=Pfam.objects.get(domain_id=domain['pfam_id'].get('domain_id'))
            ProteinDomain.objects.create(protein=protein, 
                                        pfam_id=pfam, 
                                        description=domain.get('description'),
                                        start=domain.get('start'),
                                        stop=domain.get('stop')
                                        )
        return protein


class ProteinListSerializer(serializers.ModelSerializer):
    """
    Serializer that includes id and protein_id of a Protein
    """

    class Meta:
        model = Protein
        fields = ['id', 'protein_id']

class ProteinDomainListSerializer(serializers.ModelSerializer):
    """
    Serializer that includes id of ProteinDomain and pfam_id
    """

    pfam_id = PfamSerializer(many=False, read_only=True)

    class Meta:
        model = ProteinDomain
        fields = ['id', 'pfam_id']

class ProteinAndProteinDomainListSerializer(serializers.ModelSerializer):
    """
    Serializer that includes ProteinDomain id and protein_id
    """

    protein_id = serializers.CharField(source='protein.protein_id', read_only=True)

    class Meta:
        model = ProteinDomain
        fields = ['id', 'protein_id']

            


