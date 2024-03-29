from django.shortcuts import render
from django.db.models import Count
from django_tables2 import RequestConfig
import django_tables2 as tables
from django.db.models import Q

from base.views import marker_color
from main.models import Species, Population
from main.models import Phenotype, Individual
from main.models import PlantImage, Accession
from main.tables import PopulationTable, PhenotypeTable, IndividualsTable
from main.tables import ImageTable, IndividualPhenotypeTable, PhenotypeValueTable
from main.tables import PhenotypeValueTableCultivated, AccessionTable
from main.tables import AccessionPhenotypeTable
from main.forms import PopulationFilter, PhenotypeFilter
from base.views import marker_color

import json
import numpy as np
from scipy.stats import norm, probplot
'''
Species Overview Page
'''
def species_overview(request):
    species = Species.objects.all().order_by('ncbi_id')
    return render(request,'main/species_overview.html',{"species":species})

'''
Species Detailed Page
'''
def species_details(request, ncbi_id):
    try:
        vdata = {}
        species = Species.objects.get(ncbi_id=ncbi_id)
        pops = species.population_set.all()
        
        if species.cultivated:
            obs = species.accession_set.annotate(count_phenotypes=Count('phenotypelink__phenotypevalue__phenotype',distinct=True)).all()
            acc_table = AccessionTable(obs)
            RequestConfig(request, paginate={"per_page":50}).configure(acc_table)
            vdata['acc_table'] = acc_table
        else:
            obs = species.individual_set.annotate(count_phenotypes=Count('phenotypelink__phenotypevalue__phenotype',distinct=True)).all()
            ind_table = IndividualsTable(obs)
            RequestConfig(request, paginate={"per_page":50}).configure(ind_table)
            data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")"} for pop in pops]   
            vdata['map_data'] = json.dumps(data)
            vdata['ind_table'] = ind_table
        
        pop_table = PopulationTable(pops, order_by="population_id")
        RequestConfig(request, paginate={"per_page":50}).configure(pop_table)
        pheno_table = PhenotypeTable(species.phenotype_set.all())
        RequestConfig(request, paginate={"per_page":50}).configure(pheno_table)
        
        vdata['message'] = "ok"
        vdata['ncbi_id'] = ncbi_id
        vdata['species'] = species
        vdata['pop_table'] = pop_table
        vdata['pheno_table'] = pheno_table
        return render(request,'main/species_detail.html',vdata)
    except:
        return render(request,'main/species_detail.html',{"message":"no_species","ncbi_id":ncbi_id})

'''
Population Overview Page
'''
def population_overview(request):
    
    initial = {}

    if request.method == 'POST':
        form = PopulationFilter(request.POST)
        search_dict = {}
        species = request.POST.get('species')
        if not (species==None or species==""):
            search_dict['species__species'] = species
            initial['species'] = species
        country = request.POST.get('country')
        if not ( country==None or country==""):
            search_dict['country'] = country
            initial['country'] = country
        sitename = request.POST.get('sitename')
        if not ( sitename==None or sitename==""):
            search_dict['sitename'] = sitename
            initial['sitename'] = sitename
        cultivated = request.POST.get('cultivated')
        if not ( cultivated==None or cultivated==""):
            search_dict['species__cultivated'] = cultivated
            initial['cultivated'] = cultivated
        pops = Population.objects.filter(**search_dict)
    else:
        pops = Population.objects.all()
        

    data = []
    for pop in pops:
        if pop.species.cultivated==False:
            data.append({"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")", "style": {"fill": marker_color(pop.species.species),"r":4,"opacity":0.6},"weburl":"/population/" + str(pop.population_id) + "/"})   
    table = PopulationTable(pops, order_by="population_id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)

    form = PopulationFilter(initial=initial)
    vdata = {}
    if pops.count()==0:
        vdata['filter_empty'] = True
    else:
        vdata['filter_empty'] = False
    vdata['pop_table'] = table
    vdata['map_data'] = json.dumps(data)
    #vdata['filter'] = filter
    vdata['form'] = form
    return render(request,'main/population_overview.html',vdata)

'''
Population Detail Page
'''
def population_detail(request,population_id):
    pop = Population.objects.get(population_id=population_id)
    vdata = {}
    if not pop.species.cultivated:
        data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")"}]  
        vdata['map_data'] = json.dumps(data)
    vdata['pop'] = pop
    if pop.species.cultivated:
        table = AccessionTable(pop.accession_set.annotate(count_phenotypes=Count('phenotypelink__phenotypevalue__phenotype',distinct=True)).all(), order_by="accession_id")
    else:
        table = IndividualsTable(pop.individual_set.annotate(count_phenotypes=Count('phenotypelink__phenotypevalue__phenotype',distinct=True)).all(), order_by="individual_id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)
    vdata['table'] = table
    return render(request,'main/population_detail.html',vdata)

'''
Phenotype Overview Page
'''
def phenotype_overview(request):
    initial = {}

    if request.method == 'POST':
        form = PhenotypeFilter(request.POST)
        search_dict = {}
        species = request.POST.get('species')
        if not (species==None or species==""):
            search_dict['species__species'] = species
            initial['species'] = species
        res = request.POST.get('category')
        if not ( res==None or res==""):
            search_dict['category'] = res
            initial['category'] = res
        res = request.POST.get('subcategory')
        if not ( res==None or res==""):
            search_dict['sub_category'] = res
            initial['subcategory'] = res
        cultivated = request.POST.get('cultivated')
        if not ( cultivated==None or cultivated==""):
            search_dict['species__cultivated'] = cultivated
            initial['cultivated'] = cultivated
        
        search = request.POST.get('search')
        if not (search==None or search==""):
            search = search.strip()
            initial['search'] = search
            obs = Phenotype.objects.filter(Q(**search_dict) | Q(name__contains=search) | Q(category__contains=search) |
                                           Q(sub_category__contains=search) | Q(type__contains=search) |
                                           Q(ontology__name__contains=search))
        else:
            obs = Phenotype.objects.filter(**search_dict)
    else:
        obs = Phenotype.objects.all()
    
    form = PhenotypeFilter(initial=initial)
    vdata = {}
    if obs.count()==0:
        vdata['filter_empty'] = True
    else:
        vdata['filter_empty'] = False
    
    table = PhenotypeTable(obs, order_by="id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)
    vdata['table'] = table
    vdata['form'] = form
    return render(request,'main/phenotype_overview.html',vdata)

'''
Phenotype Detail Page
'''
def phenotype_detail(request,id):
    vdata = {}
    try:
        pheno = Phenotype.objects.get(id=id)
        message = "ok"
        vdata['pheno'] = pheno
        if pheno.species.cultivated==True:
            vdata['cultivated'] = True
            value_set = pheno.phenotypevalue_set.values("phenotype_link__accession__accession_id",
                                                        "phenotype_link__accession__population_id",
                                                        "value",
                                                        "phenotype_link__accession__species__species",
                                                        "phenotype_link__accession__species__ncbi_id")
            pop_set = value_set.values("phenotype_link__accession__population_id",
                                       "phenotype_link__accession__species__species",
                                       "phenotype_link__accession__species__ncbi_id").distinct()
            vdata['map_data'] = None
            table = PhenotypeValueTableCultivated(value_set, order_by="phenotype_link__accession__accession_id")
            RequestConfig(request, paginate={"per_page":20}).configure(table)
            vdata['table'] = table
        else:
            vdata['cultivated'] = False
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
                 "style": {"fill": marker_color(elem["phenotype_link__individual__species__species"]),"r":4},
                 "weburl": "/population/" + str(elem['phenotype_link__individual__population_id']) + "/"} for elem in value_set]   
        
            vdata['map_data'] = json.dumps(data)
            vdata['pop_size'] = len(pop_set)
            
            table = PhenotypeValueTable(value_set, order_by="phenotype_link__individual__individual_id")
            RequestConfig(request, paginate={"per_page":20}).configure(table)
            vdata['table'] = table
        
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
    except:
        message = "no_pheno"
    vdata['pid'] = id
    vdata['message'] = message

    return render(request,'main/phenotype_detail.html',vdata)

'''
Individual Overview Page
'''
def individuals_overview(request):
    #.objects.annotate(count_phenotypes=Count('observationunit__phenotypevalue__phenotype', distinct=True)).prefetch_related('genotype_set').all()
    obs = Individual.objects.annotate(count_phenotypes=Count('phenotypelink__phenotypevalue__phenotype',distinct=True)).filter(species__cultivated=False)
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
    ind = Individual.objects.all()
    table = ImageTable(ind, order_by="individual_id")
    RequestConfig(request, paginate={"per_page":30}).configure(table)
    vdata = {}
    vdata['table'] = table
    return render(request,'main/image_overview.html',vdata)

'''
Accession Overview Page
'''
def accession_overview(request):
    #.objects.annotate(count_phenotypes=Count('observationunit__phenotypevalue__phenotype', distinct=True)).prefetch_related('genotype_set').all()
    obs = Accession.objects.annotate(count_phenotypes=Count('phenotypelink__phenotypevalue__phenotype',distinct=True)).filter(species__cultivated=True)
    table = AccessionTable(obs, order_by="accession_id")
    RequestConfig(request, paginate={"per_page":50}).configure(table)
    vdata = {}
    vdata['table'] = table
    return render(request,'main/accession_overview.html',vdata)

'''
Accession Detail Page
'''
def accession_detail(request,accession_id):
    ind = Accession.objects.get(accession_id=accession_id)
    pop = ind.population
    phenotype_values = ind.phenotypelink_set.values("accession__species__ncbi_id","accession__species__species",
                                                    "phenotypevalue__phenotype__name","phenotypevalue__value",
                                                    "phenotypevalue__phenotype__category","phenotypevalue__phenotype__sub_category",
                                                    "phenotypevalue__phenotype__type","phenotypevalue__phenotype_id")
    table = AccessionPhenotypeTable(phenotype_values, order_by="accession_phenotypevalue__phenotype__name")
    RequestConfig(request, paginate={"per_page":100}).configure(table)
    vdata = {}
    vdata['ind'] = ind
    vdata['table'] = table
    return render(request,'main/accession_detail.html',vdata)
