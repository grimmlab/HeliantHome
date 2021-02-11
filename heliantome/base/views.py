from django.shortcuts import render

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
    return render(request,'base/landingpage.html',vdata)
