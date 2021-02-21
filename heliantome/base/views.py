from django.shortcuts import render
import json

import main.models as models

'''
Landing Page
'''
def landing_page(request):
    vdata = {}
    vdata['number_species'] = models.Species.objects.count()
    vdata['number_phenotypes'] = models.Phenotype.objects.count()
    vdata['number_populations'] = models.Population.objects.count()
    vdata['number_individuals'] = models.Individual.objects.count()
    vdata['number_images'] = models.PlantImage.objects.count()
    
    pops = models.Population.objects.all()
    data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")"} for pop in pops]   
    vdata['map_data'] = json.dumps(data)

    return render(request,'base/landingpage.html',vdata)

'''
About Page
'''
def about_page(request):
    return render(request,'base/about.html',{})
