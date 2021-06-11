from django.shortcuts import render
import json

import main.models as models

def marker_color(species):
    if species == "Helianthus annuus":
        return "#1dad54"
    elif species == "Helianthus annuus subsp. texanus":
        return "#fa9d14"
    elif species == "Helianthus argophyllus":
        return "#3c1d64"
    elif species == "Helianthus petiolaris subsp. fallax":
        return "#1a57e1"
    elif species == "Helianthus petiolaris subsp. petiolaris":
        return "#af1384"
    elif species == "Helianthus niveus subsp. canescens":
        return "#cd6750"
    else:
        return "yellow"


'''
Landing Page
'''
def landing_page(request):
    vdata = {}
    vdata['number_species'] = models.Species.objects.count()
    vdata['number_phenotypes'] = models.Phenotype.objects.count()
    vdata['number_measurements'] = models.PhenotypeValue.objects.count()
    vdata['number_populations'] = models.Population.objects.count()
    vdata['number_individuals'] = models.Individual.objects.count()
    vdata['number_images'] = models.PlantImage.objects.count()
    
    pops = models.Population.objects.all()
    data = [{"latLng": [pop.latitude, pop.longitude], "name": pop.species.species + ": " + pop.population_id + " (" + pop.country + ", " + pop.sitename + ")", "style": {"fill": marker_color(pop.species.species),"r":4}} for pop in pops]   
    vdata['map_data'] = json.dumps(data)

    return render(request,'base/landingpage.html',vdata)

'''
About Page
'''
def about_page(request):
    return render(request,'base/about.html',{})
