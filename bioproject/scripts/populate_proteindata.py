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
        # store protein_id as the key which is associated to a list with 3 elements
        # this dataset only contains the first element: the sequence
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
            # store taxa_id as the key which is associated to a list of values that contain
            # [0] clade [1] genus and [2] species
            taxonomy[row[1]] = [row[2], genus_species_pairs[0], genus_species_pairs[1]]
        # add domain
        if row[5] not in domain.keys():
            # store domain_id as the key which is associated with a domain description
            domain[row[5]] = row[4]
        # protein data
        if row[0] not in protein.keys():
            # if the protein key does not already exist, then it was not included in the
            # dataset with protein sequences.
            protein[row[0]] = ['', row[1], row[8]]
        else:
            # if its already included then the protein sequence is already stored.
            # the list stores [0] sequence, [1] taxonomy id and [2] length
            protein[row[0]][1] = row[1]
            protein[row[0]][2] = row[8]
        # store the start and stop of each protein and domain pair
        # therefore, the key is a protein and domain tuple
        proteindomain[(row[0], row[5])] = [row[6], row[7]]


ProteinDomain.objects.all().delete()
Protein.objects.all().delete()
Pfam.objects.all().delete()
Taxonomy.objects.all().delete()

pfam_rows = {}
taxonomy_rows = {}
protein_rows = {}
proteindomain_rows = {}

# Create pfam objects
pfam_list = [
    Pfam(
        domain_id = pfam_id,
        domain_description = pfam_desc
    )
    for pfam_id, pfam_desc in pfam
]
pfam_objs = Pfam.objects.bulk_create(pfam_list)
pfam_rows = {x.domain_id:x for x in Pfam.objects.all()}
print('Pfam objects created')


# Create taxonomy objects
taxa_list = [
    Taxonomy(
        taxa_id = taxa_id,
        clade = data[0],
        genus = data[1],
        species = data[2]
    )
    for taxa_id, data in taxonomy.items()
]
taxa_objs = Taxonomy.objects.bulk_create(taxa_list)
taxonomy_rows = {x.taxa_id:x for x in Taxonomy.objects.all()}
print('Taxonomy objects created')

# Create protein objects
protein_list = [
    Protein(
        protein_id = protein_id,
        sequence = data[0],
        taxonomy = taxonomy_rows[data[1]],
        length = data[2]
    )
    for protein_id, data in protein.items()
]
protein_objs = Protein.objects.bulk_create(protein_list)
protein_rows = {x.protein_id:x for x in Protein.objects.all()}
print('Protein objects created')

# Create protein_domain objects
protein_domain_list = [
    ProteinDomain(
        protein = protein_rows[protein_domain[0]], 
        start = data[0],
        stop = data[1],
        pfam_id = pfam_rows[protein_domain[1]],
        description = domain[protein_domain[1]]
    )
    for protein_domain, data in proteindomain.items()
]
protein_domain_objs = ProteinDomain.objects.bulk_create(protein_domain_list)
print('ProteinDomain objects created')
