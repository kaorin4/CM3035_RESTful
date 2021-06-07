from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # cross site validation exemption
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *

from django.db.models import FloatField

# GET request
# receives protein_id as parameter
# returns the detail of that protein
class ProteinDetails(generics.RetrieveAPIView):

    lookup_field = 'protein_id'
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer


# GET request
# receives pfam_id as parameter
# returns the domain_id and it's description
class PfamDetails(generics.RetrieveAPIView):

    lookup_field = 'domain_id'
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer


class FilterProteinByTaxonomy(generics.ListAPIView):
    
    queryset = Protein.objects.all().distinct()
    serializer_class = ProteinListSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(taxonomy__taxa_id=self.kwargs.get('taxa_id'))


class FilterDomainByTaxonomy(generics.ListAPIView):
    
    queryset = ProteinDomain.objects.all()
    serializer_class = ProteinDomainListSerializer

    """
    Retrieve the list of domains of a given taxonomy_id
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

    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

# class PostProteinDetails(generics.CreateAPIView):

#     queryset = Protein.objects.all()
#     serializer_class = ProteinSerializer
#     permission_classes = ()
#     authentication_classes = ()

#     # def post(self, request, *args, **kwargs):
#     #     return self.create(request, *args, **kwargs)

#     def create(self, request, *args, **kwargs):
#         protein_form = ProteinForm(request.data)
#         if protein_form.is_valid():
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             # data = serializer.validated_data
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'errors': protein_form.errors}, status=400)


#     # def create(self, request, *args, **kwargs):
#     #     serializer = self.get_serializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     self.perform_create(serializer)
#     #     headers = self.get_success_headers(serializer.data)
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     # def perform_create(self, serializer):
#     #     serializer.save()

#     # def get_success_headers(self, data):
#     #     try:
#     #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#     #     except (TypeError, KeyError):
#     #         return {}






