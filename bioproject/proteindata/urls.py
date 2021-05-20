from django.urls import include, path
from . import views
from . import api


urlpatterns = [
    # path('', views.index, name = 'index'),
    path('api/protein/<str:protein_id>/', api.ProteinDetails.as_view(), name='protein_api'),
    path('api/pfam/<str:domain_id>/', api.PfamDetails.as_view(), name='pfam_api'),
    path('api/proteins/<str:taxa_id>/', api.FilterProteinByTaxonomy.as_view(), name='protein_tax_api'),
    path('api/pfams/<str:taxa_id>/', api.FilterDomainByTaxonomy.as_view(), name='domain_tax_api'),
    path('api/coverage/<str:protein_id>/', api.ProteinCoverage.as_view(), name='protein_coverage'),
    path('api/protein/', api.PostProteinDetails.as_view(), name='protein_api'),
]