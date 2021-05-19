from django.urls import include, path
from . import views
from . import api

from . import views

urlpatterns = [
    # path('', views.index, name = 'index'),
    path('api/protein/<str:protein_id>/', api.ProteinDetails.as_view(), name='protein_api'),
    path('api/pfam/<str:domain_id>/', api.PfamDetails.as_view(), name='pfam_api'),
    path('api/proteins/<str:taxa_id>/', api.FilterProteinByTaxonomy.as_view(), name='protein_tax_api'),
    # path('api/proteins/(?P<username>.+)/', api.ProteinByTaxonomy.as_view(), name='protein_tax_api'),
]