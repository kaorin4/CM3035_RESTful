from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # cross site validation exemption
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *

# GET request
# returns the domain id and it's description
class PfamDetails(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):

    lookup_field = 'domain_id'
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ProteinDetails(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    lookup_field = 'protein_id'
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer

    # each of the functions we want implemented
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class FilterProteinByTaxonomy(generics.ListAPIView):
    
    queryset = Protein.objects.all().distinct()
    serializer_class = ProteinListSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(taxonomy__taxa_id=self.kwargs.get('taxa_id'))


class FilterDomainByTaxonomy(generics.ListAPIView):
    
    queryset = ProteinDomain.objects.all()
    serializer_class = ProteinDomainListSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(protein__taxonomy__taxa_id=self.kwargs.get('taxa_id'))

class ProteinCoverage(generics.GenericAPIView):
    """
    Retrieve list of transactions
    """
    def get(self, request, protein_id):
        """List Transactions"""
        # protein = Protein.objects.get(protein__protein_id=protein_id)
        # serializer = ProteinSerializer(proteins, many=True)

        domains = ProteinDomain.objects.filter(protein__protein_id=protein_id)
        protein = Protein.objects.get(protein_id=protein_id)
        start_sum = domains.all().aggregate(models.Sum('start'))
        stop_sum = domains.all().aggregate(models.Sum('stop'))
        length = protein.length
        coverage = (start_sum['start__sum'] - stop_sum['stop__sum'])/length
        # print(start_sum)
        return Response(abs(coverage))
        
        # return_data = sum([lambda items: items['amount']])
        # return Response(return_data)




