from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # cross site validation exemption
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *

from django.db.models import FloatField

class ProteinDetails(generics.RetrieveDestroyAPIView):
    """
    GET request
    receives protein_id as parameter
    returns the detail of that protein
    
    DELETE request
    receives protein_id as parameter
    deletes the selected protein
    """

    lookup_field = 'protein_id'
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer


class PfamDetails(generics.RetrieveAPIView):
    """
    GET request
    receives pfam_id as parameter
    returns the domain_id and it's description
    """

    lookup_field = 'domain_id'
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer


class FilterProteinByTaxonomy(generics.ListAPIView):
    """
    GET request
    receives taxa_id as parameter
    return a list of all proteins for a given organism
    """
    queryset = Protein.objects.all().distinct()
    serializer_class = ProteinListSerializer

    """
    Filter proteins by taxa_id
    """
    def filter_queryset(self, queryset):
        return queryset.filter(taxonomy__taxa_id=self.kwargs.get('taxa_id'))

class FilterProteinDomainByTaxonomy(generics.ListAPIView):
    """
    GET request
    receives taxa_id as parameter
    return a list of all protein_id and protein domain id for a given organism
    """
    queryset = ProteinDomain.objects.all()
    serializer_class = ProteinAndProteinDomainListSerializer

    """
    Filter the list of protein domains of a given taxa_id
    """
    def filter_queryset(self, queryset):
        return queryset.filter(protein__taxonomy__taxa_id=self.kwargs.get('taxa_id'))


class FilterDomainByTaxonomy(generics.ListAPIView):
    """
    GET request
    receives taxa_id as parameter
    return a list of all domains for a given organism
    """
    queryset = ProteinDomain.objects.all()
    serializer_class = ProteinDomainListSerializer

    """
    Retrieve the list of domains of a given taxa_id
    """
    def filter_queryset(self, queryset):
        return queryset.filter(protein__taxonomy__taxa_id=self.kwargs.get('taxa_id'))

class ProteinCoverage(generics.GenericAPIView):
    """
    Retrieve the domain coverage for a given protein. That is Sum of the protein domain lengths (start-stop)/length of protein.
    """
    def get(self, request, protein_id):

        domains = ProteinDomain.objects.filter(protein__protein_id=protein_id)
        protein = Protein.objects.get(protein_id=protein_id)
        length = protein.length
        result = domains.aggregate(difference=models.Sum('start') - models.Sum('stop'))
        
        coverage = result['difference']/length

        return Response(abs(coverage))

class PostProteinDetails(generics.CreateAPIView):
    """
    POST request
    Creates a new protein object as well as its corresponding proteindomain objects
    """
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer




