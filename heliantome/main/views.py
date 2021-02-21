from django.shortcuts import render

from main.models import Species

'''
Species Overview Page
'''
def species_overview(request):
    species = Species.objects.all()
    return render(request,'main/species_overview.html',{"species":species})
