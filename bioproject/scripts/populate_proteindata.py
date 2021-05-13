import os
import sys
import django
import csv
from collections import defaultdict

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# sys.path.append('/home/coder/project/awd_midterm/bioproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioproject.settings')
django.setup()

from proteindata.models import *

pfam_data_file = '../datasets/pfam_descriptions.csv'
assignment_data_file = '../datasets/assignment_data_set.csv'
assignment_sequences_data_file = '../datasets/assignment_data_sequences.csv'

pfam = set() #2453
taxonomy = defaultdict(list) #1995
domain = defaultdict() #2453
protein = defaultdict(list) #9988
proteindomain = defaultdict(list)

# to open and store data from assignment_data_sequences.csv file
with open(assignment_sequences_data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        protein[row[0]] = [row[1], '', '']

# to open and store data from pfam_descriptions.csv file
with open(pfam_data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        pfam.add((row[0], row[1]))

# to open and store data from assignment_data_set.csv file
with open(assignment_data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        # add taxonomies if tax is already not included in the dict
        if row[1] not in taxonomy.keys():
            # split genus species column into two: genus and species
            genus_species_pairs = row[3].split()
            taxonomy[row[1]] = [row[2], genus_species_pairs[0], genus_species_pairs[1]]
        # add domain
        if row[5] not in domain.keys():
            domain[row[5]] = row[4]
        # protein data
        if row[0] not in protein.keys():
            protein[row[0]] = ['', row[1], row[8]]
        else:
            protein[row[0]][1] = row[1]
            protein[row[0]][2] = row[8]
            # print(protein[row[0]])
        if row[0] not in proteindomain.keys():
            proteindomain[row[0]] = [[row[5]], row[6], row[7]]
        else:
            proteindomain[row[0]][0].append(row[5])


# ProteinDomain.objects.all().delete()
# Protein.objects.all().delete()
# Domain.objects.all().delete()
# Pfam.objects.all().delete()
# Taxonomy.objects.all().delete()


pfam_rows = {}
taxonomy_rows = {}
domain_rows = {}
protein_rows = {}
proteindomain_rows = {}

print(len(taxonomy))
print(len(pfam))
print(len(domain))
print(len(proteindomain))


# for pfam_id, pfam_desc in pfam:
#     row = Pfam.objects.create(domain_id = pfam_id, domain_description = pfam_desc)
#     row.save()
#     pfam_rows[pfam_id] = row

#     row_domain = Domain.objects.create(pfam_id = pfam_rows[pfam_id], 
#                             description = domain[pfam_id])
#     row.save()
#     domain_rows[pfam_id] = row

# for taxa_id, data in taxonomy.items():
#     row = Taxonomy.objects.create(taxa_id = taxa_id, 
#                                 clade = data[0],
#                                 genus = data[1],
#                                 species = data[2])
#     row.save()
#     taxonomy_rows[taxa_id] = row

# for domain_id, description in domain.items():
#     row = Domain.objects.create(pfam_id = pfam_rows[domain_id], 
#                                 description = description)
#     row.save()
#     domain_rows[domain_id] = row


for item in Pfam.objects.all():
    pfam_rows[item.domain_id] = item


for item in Domain.objects.all():
    domain_rows[item.pfam_id.domain_id] = item

for item in Taxonomy.objects.all():
    taxonomy_rows[item.taxa_id] = item

for item in Protein.objects.all():
    protein_rows[item.protein_id] = item


# for protein_id, data in protein.items():
#     row = Protein.objects.create(protein_id = protein_id, 
#                                 sequence = data[0],
#                                 taxonomy = taxonomy_rows[data[1]],
#                                 length = data[2])
#     print(protein_id)
#     row.save()
#     protein_rows[protein_id] = row

for protein_id, data in proteindomain.items():
    for domain_id in proteindomain[protein_id][0]:
        row = ProteinDomain.objects.create(protein = protein_rows[protein_id], 
                                    start = data[1],
                                    stop = data[2],
                                    domain = domain_rows[domain_id])
        row.save()
        proteindomain_rows[protein_id] = row




