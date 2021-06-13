from django.shortcuts import render
from django.db.models import Count
from django_tables2 import RequestConfig
import django_tables2 as tables

from base.views import marker_color
from main.models import Species, Population
from main.models import Phenotype, Individual
from main.models import PlantImage
from main.tables import PopulationTable, PhenotypeTable, IndividualsTable
from main.tables import ImageTable, IndividualPhenotypeTable, PhenotypeValueTable

import json
import numpy as np
from scipy.stats import norm, probplot
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
    vdata = {}
    #try:
    if 1:
        pheno = Phenotype.objects.get(id=id)
        message = "ok"
        vdata['pheno'] = pheno
        value_set = pheno.phenotypevalue_set.values("phenotype_link__individual__individual_id",
                                                    "phenotype_link__individual__population_id",
                                                    "phenotype_link__individual__population__latitude",
                                                    "phenotype_link__individual__population__longitude",
                                                    "phenotype_link__individual__population__country",
                                                    "phenotype_link__individual__population__sitename","value",
                                                    "phenotype_link__individual__species__species",
                                                    "phenotype_link__individual__species__ncbi_id")
        pop_set = value_set.values("phenotype_link__individual__population_id",
                                   "phenotype_link__individual__population__latitude",
                                   "phenotype_link__individual__population__longitude",
                                   "phenotype_link__individual__population__country",
                                   "phenotype_link__individual__population__sitename",
                                   "phenotype_link__individual__species__species",
                                   "phenotype_link__individual__species__ncbi_id").distinct()
        data = [{"latLng": [elem['phenotype_link__individual__population__latitude'], 
                            elem["phenotype_link__individual__population__longitude"]], 
                 "name": elem["phenotype_link__individual__species__species"] + ": " + 
                         elem['phenotype_link__individual__population_id'] + " (" + 
                         elem['phenotype_link__individual__population__country'] + ", " + 
                         elem['phenotype_link__individual__population__sitename'] + ")",
                 "style": {"fill": marker_color(elem["phenotype_link__individual__species__species"]),"r":4}} for elem in value_set]   
        
        vdata['map_data'] = json.dumps(data)
        vdata['pop_size'] = len(pop_set)
        values = value_set.values_list("value",flat=True)
        #compute hist
        hist, bins = np.histogram(values,bins=30,density=True)
        #fit normal curve
        mu, std = norm.fit(values)
        x = np.linspace(min(bins), max(bins), len(bins))
        p = norm.pdf(x, mu, std)
        vdata['hist'] = json.dumps(list(np.array(hist,dtype="float")))
        vdata['bins'] = json.dumps(list(np.array(np.round(bins,2),dtype="float")))
        vdata['p'] = json.dumps(list(np.array(p,dtype="float")))
        vdata['mu'] = np.round(mu,2)
        vdata['std'] = np.round(std)
        
        #qq-plot
        #ndist = norm.rvs(loc=mu, scale=std,size = len(values))
        #ndist = np.array([ norm.ppf(i / len(values),loc=mu,scale=std) for i in range(1, len(values)) ])
        #ndist = np.arange(0,len(values)+1)
        #ndist.sort()
        osm, osr = probplot(values)
        ndist = osm[0]
        vdata['ndist'] = json.dumps(list(np.array(ndist,dtype="float")))
        #vsort = np.sort(values)
        vsort = osm[1]
        vdata['vsort'] = json.dumps(list(np.array(vsort,dtype="float")))
        y_min_value = min(vsort)
        y_max_value = max(vsort)
        x_min_value = min(ndist)
        x_max_value = max(ndist)
        vdata['x_min_value'] = x_min_value
        vdata['x_max_value'] = x_max_value
        vdata['y_min_value'] = y_min_value
        vdata['y_max_value'] = y_max_value
        diagonal = np.interp(ndist, [x_min_value,x_max_value], [y_min_value,y_max_value])
        vdata['diagonal_qq'] = json.dumps(list(np.array(diagonal,dtype="float")))
        table = PhenotypeValueTable(value_set, order_by="phenotype_link__individual__individual_id")
        RequestConfig(request, paginate={"per_page":50}).configure(table)
        vdata['table'] = table
    #except:
    #    message = "no_pheno"
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
