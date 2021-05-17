from django.urls import include, path
from . import views
from . import api

from . import views

urlpatterns = [
    # path('', views.index, name = 'index'),
    path('api/pfam/<str:domain_id>/', api.PfamDetails.as_view(), name='pfam_api'),
]