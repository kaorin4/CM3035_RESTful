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



