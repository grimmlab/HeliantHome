from django.shortcuts import render
from django.db.models import Count
from django_tables2 import RequestConfig
import django_tables2 as tables


from main.models import Species, Population
from main.models import Phenotype, Individual
from main.models import PlantImage
from main.tables import PopulationTable, PhenotypeTable, IndividualsTable
from main.tables import ImageTable, IndividualPhenotypeTable

import json

'''
Species Overview Page
'''
def species_overview(request):
    species = Species.objects.all()
    return render(request,'main/species_overview.html',{"species":species})

'''
Species Detailed Page
'''
def species_details(request, ncbi_id):
    try:
        species = Species.objects.get(ncbi_id=ncbi_id)
        pops = Population.objects.filter(species=species)
        data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")"} for pop in pops]   
        vdata = {}
        vdata['map_data'] = json.dumps(data)
        vdata['message'] = "ok"
        vdata['ncbi_id'] = ncbi_id
        vdata['species'] = species
        return render(request,'main/species_detail.html',vdata)
    except:
        return render(request,'main/species_detail.html',{"message":"no_species","ncbi_id":ncbi_id})

'''
Population Overview Page
'''
def population_overview(request):
    pops = Population.objects.all()
    data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")"} for pop in pops]   
    table = PopulationTable(pops, order_by="population_id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)
    vdata = {}
    vdata['pop_table'] = table
    vdata['map_data'] = json.dumps(data)
    return render(request,'main/population_overview.html',vdata)

'''
Population Detail Page
'''
def population_detail(request,population_id):
    pop = Population.objects.get(population_id=population_id)
    data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")"}]  
    vdata = {}
    vdata['map_data'] = json.dumps(data)
    return render(request,'main/population_detail.html',vdata)

'''
Phenotype Overview Page
'''
def phenotype_overview(request):
    obs = Phenotype.objects.all()
    table = PhenotypeTable(obs, order_by="id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)
    vdata = {}
    vdata['table'] = table
    return render(request,'main/phenotype_overview.html',vdata)

'''
Phenotype Detail Page
'''
def phenotype_detail(request,id):
    try:
        pheno = Phenotype.objects.get(id=id)
        message = "ok"
    except:
        pheno = None
        message = "no_pheno"
    vdata = {}
    vdata['pheno'] = pheno
    vdata['pid'] = id
    vdata['message'] = message
    return render(request,'main/phenotype_detail.html',vdata)

'''
Individual Overview Page
'''
def individuals_overview(request):
    #.objects.annotate(count_phenotypes=Count('observationunit__phenotypevalue__phenotype', distinct=True)).prefetch_related('genotype_set').all()
    obs = Individual.objects.annotate(count_phenotypes=Count('phenotypelink__phenotypevalue__phenotype',distinct=True)).all()
    table = IndividualsTable(obs, order_by="individual_id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)
    vdata = {}
    vdata['table'] = table
    return render(request,'main/individuals_overview.html',vdata)

'''
Individual Detail Page
'''
def individual_detail(request,individual_id):
    ind = Individual.objects.get(individual_id=individual_id)
    pop = ind.population
    phenotype_values = ind.phenotypelink_set.values("individual__species__ncbi_id","individual__species__species",
                                                    "phenotypevalue__phenotype__name","phenotypevalue__value",
                                                    "phenotypevalue__phenotype__category","phenotypevalue__phenotype__sub_category",
                                                    "phenotypevalue__phenotype__type","phenotypevalue__phenotype_id")
    table = IndividualPhenotypeTable(phenotype_values, order_by="individual_phenotypevalue__phenotype__name")
    RequestConfig(request, paginate={"per_page":100}).configure(table)
    data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")"}]  
    vdata = {}
    vdata['map_data'] = json.dumps(data)
    vdata['ind'] = ind
    vdata['table'] = table
    return render(request,'main/individual_detail.html',vdata)

'''
Image Overview Page
'''
def image_overview(request):
    images = PlantImage.objects.all()
    table = ImageTable(images, order_by="individual_id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)
    vdata = {}
    vdata['table'] = table
    return render(request,'main/image_overview.html',vdata)
