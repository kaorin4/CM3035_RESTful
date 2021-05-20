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

    def create(self, validated_data):
        taxonomy_data = validated_data.get('taxonomy')
        protein_domains_data = validated_data.pop('domain_to_protein')
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

    class Meta:
        model = Protein
        fields = ['id', 'protein_id']

class ProteinDomainListSerializer(serializers.ModelSerializer):

    pfam_id = PfamSerializer(many=False, read_only=True)

    class Meta:
        model = ProteinDomain
        fields = ['id', 'pfam_id']
