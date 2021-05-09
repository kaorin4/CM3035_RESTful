from django.db import models

# Create your models here.

class Pfam(models.Model):
    domain_id = models.CharField(max_length=256, null=False, blank=False, db_index=True)
    domain_description = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.domain_id


class Domain(models.Model):
    description = models.CharField(max_length=256, null=False, blank=False)
    start = models.IntegerField(null=False, blank=True)
    stop = models.IntegerField(null=False, blank=True)
    pfam_id = models.ForeignKey(Pfam, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.description

class Taxonomy(models.Model):
    taxa_id = models.CharField(max_length=256, null=False, blank=False, db_index=True)
    clade = models.CharField(max_length=256, null=False, blank=False)
    genus = models.CharField(max_length=256, null=False, blank=False)
    species = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.taxa_id

class Protein(models.Model):
    protein_id = models.CharField(max_length=256, null=False, blank=False, db_index=True)
    sequence = models.CharField(max_length=256, null=False, blank=False)
    length = models.IntegerField(null=False, blank=True)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING)
    domains = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.taxa_id
