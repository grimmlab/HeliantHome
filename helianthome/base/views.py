from django.shortcuts import render

import json
import numpy as np

import main.models as models

def marker_color(species):
    if species == "Helianthus annuus":
        #return "#1dad54"
        return "#C9A42E"
    elif species == "Helianthus annuus subsp. texanus":
        return "#fa9d14"
    elif species == "Helianthus argophyllus":
        return "#3C813E"
        #return "#af1384"
    elif species == "Helianthus petiolaris subsp. fallax":
        #return "#1a57e1"
        return "#496A89"
    elif species == "Helianthus petiolaris subsp. petiolaris":
        return "#57AFA6"
    elif species == "Helianthus niveus subsp. canescens":
        return "#496A89"
    else:
        return "yellow"


'''
Landing Page
'''
def landing_page(request):
    #search_form = GlobalSearchForm()
    #if "global_search-autocomplete" in request.POST:
    #    query = request.POST.getlist('global_search-autocomplete')[0]
    #    return HttpResponseRedirect("search_results/%s/"%(query))
    vdata = {}
    #vdata['search_form'] = search_form
    vdata['number_species'] = models.Species.objects.filter().count()
    vdata['number_cultivated'] = models.Species.objects.filter(cultivated=True).count()
    vdata['number_phenotypes'] = models.Phenotype.objects.count()
    vdata['number_measurements'] = models.PhenotypeValue.objects.count()
    vdata['number_populations'] = models.Population.objects.count()
    vdata['number_individuals'] = models.Individual.objects.count()
    vdata['number_accessions'] = models.Accession.objects.count()
    vdata['number_images'] = models.PlantImage.objects.count()
    categories = models.Phenotype.objects.values_list("category").distinct()
    category_list = []
    category_entries = []
    for cat in categories:
        category_list.append(str(cat[0]))
        category_entries.append(models.Phenotype.objects.filter(category=cat[0]).count())
    vdata['category_list'] = json.dumps(category_list)
    vdata['category_entries'] = json.dumps(list(np.array(category_entries,dtype="float")))
    pops = models.Population.objects.filter(species__cultivated=False)
    data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")", "style": {"fill": marker_color(pop.species.species),"r":4,"opacity":0.8}} for pop in pops]   
    vdata['map_data'] = json.dumps(data)
    return render(request,'base/landingpage.html',vdata)

'''
About Page
'''
def about_page(request):
    return render(request,'base/about.html',{})

'''
Download Page
'''
def download_page(request):
    return render(request,'base/download.html',{})

'''
FAQ Page
'''
def faq_page(request):
    return render(request,'base/faq.html',{})

'''
Search Result View for Global Search in AraPheno
'''
def SearchResults(request,query=None):
    if query==None:
        pass
        ##phenotypes = Phenotype.objects.published().all()
        #studies = Study.objects.published().all()
        #accessions = Accession.objects.all()
        #ontologies = OntologyTerm.objects.all()
        #download_url = "/rest/search"
    else:
        pass
        #phenotypes = Phenotype.objects.published().filter(Q(name__icontains=query) |
        #                                      Q(to_term__id__icontains=query) |
        #                                      Q(to_term__name__icontains=query))
        #studies = Study.objects.published().filter(name__icontains=query)
        #accessions = Accession.objects.filter(name__icontains=query)
        #ontologies = OntologyTerm.objects.filter(name__icontains=query)
        #download_url = "/rest/search/" + str(query)

    #phenotype_table = PhenotypeTable(phenotypes,order_by="-name")
    #RequestConfig(request,paginate={"per_page":10}).configure(phenotype_table)

    #study_table = StudyTable(studies,order_by="-name")
    #RequestConfig(request,paginate={"per_page":10}).configure(study_table)

    #accession_table = AccessionTable(accessions,order_by="-name")
    #RequestConfig(request,paginate={"per_page":10}).configure(accession_table)

    #ontologies_table = OntologyTermTable(ontologies,order_by="-name")
    #RequestConfig(request,paginate={"per_page":10}).configure(ontologies_table)

    variable_dict = {}
    variable_dict['query'] = query
    #variable_dict['nphenotypes'] = phenotypes.count()
    #variable_dict['phenotype_table'] = phenotype_table
    #variable_dict['accession_table'] = accession_table
    #variable_dict['ontologies_table'] = ontologies_table
    #variable_dict['study_table'] = study_table

    #variable_dict['nstudies'] = studies.count()
    #variable_dict['naccessions'] = accessions.count()
    #variable_dict['nontologies'] = ontologies.count()
    #variable_dict['download_url'] = download_url

    return render(request,'base/search_results.html',variable_dict)

