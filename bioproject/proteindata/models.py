from django.db import models

# Create your models here.

class Pfam(models.Model):
    domain_id = models.CharField(max_length=256, null=False, blank=False)
    domain_description = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.domain_id

class Taxonomy(models.Model):
    taxa_id = models.CharField(max_length=256, null=False, blank=False)
    clade = models.CharField(max_length=256, null=False, blank=False)
    genus = models.CharField(max_length=256, null=False, blank=False)
    species = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        verbose_name_plural = "taxonomies"

    def __str__(self):
        return self.taxa_id

class Protein(models.Model):
    protein_id = models.CharField(max_length=256, null=False, blank=False)
    sequence = models.CharField(max_length=256, null=False, blank=False)
    length = models.IntegerField(null=False, blank=True)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING)
    domains = models.ManyToManyField(Pfam, through='ProteinDomain')

    def __str__(self):
        return self.protein_id

class ProteinDomain(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='domain_to_protein')
    pfam_id = models.ForeignKey(Pfam, on_delete=models.CASCADE, related_name='protein_to_domain')
    description = models.CharField(max_length=256, null=False, blank=False)
    start = models.IntegerField(null=False, blank=True)
    stop = models.IntegerField(null=False, blank=True)
