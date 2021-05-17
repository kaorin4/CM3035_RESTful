from django.contrib import admin
from .models import *

# Register your models here.

class PfamAdmin(admin.ModelAdmin):
    model = Pfam

class TaxonomyAdmin(admin.ModelAdmin):
    model = Taxonomy

class ProteinDomainAdmin(admin.ModelAdmin):
    model = ProteinDomain

class ProteinDomainInline(admin.TabularInline):
    model = Protein.domains.through

class ProteinAdmin(admin.ModelAdmin):
    model = Protein
    inlines = [
        ProteinDomainInline,
    ]
    exclude = ('domains',)

admin.site.register(Pfam, PfamAdmin)
admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(ProteinDomain, ProteinDomainAdmin)
admin.site.register(Protein, ProteinAdmin)
