import h5py
import numpy as np
from main.models import ClimateVariable, SoilVariable, Population, Individual
from datetime import datetime

TAXONOMY = {"Helianthus annuus":4232,
            "Helianthus argophyllus":73275,
            "Helianthus annuus subsp. texanus":1312900,
            "Helianthus petiolaris subsp. fallax":74150,
            "Helianthus petiolaris subsp. petiolaris":74151,
            "Helianthus niveus subsp. canescens":74145}

"""
Read and Store Climate Variables
"""
def store_climate_variables(filename="../data/climate_variables.csv"):
    f = open(filename,"r",encoding="utf-8")
    for i,line in enumerate(f):
        if i!=0:
            sv = line.strip().split(";")
            cv = ClimateVariable(id=sv[0].strip(),description=sv[1].strip())
            cv.save()
    f.close()
    print("Stored Climate Variables")

"""
Read and Store Soil Variables
"""
def store_soil_variables(filename="../data/soil_variables.csv"):
    f = open(filename,"r",encoding="utf-8")
    for i,line in enumerate(f):
        if i!=0:
            sv = line.strip().split(";")
            cv = SoilVariable(id=sv[0].strip(),description=sv[1].strip())
            cv.save()
    f.close()
    print("Stored Soil Variables")

"""
Load Phenotype Descriptions
"""
def load_phenotype_descriptions(filename="../data/phenotype_description.csv"):
    f = open(filename,"r",encoding="utf-8")
    phenotypes = {}
    for i,line in enumerate(f):
        if i!=0:
            sv = line.strip().split(";")
            phenotype = {'category':sv[0].strip(),
                         'sub_category':sv[1].strip(),
                         'ontology_name':sv[2].strip(),
                         'ontology_id':sv[3].strip().split("/")[-1],
                         'name':sv[4].strip(),
                         'unit':sv[5].strip(),
                         'description':sv[6].strip(),
                         'method':sv[7].strip(),
                         'image':sv[8].strip()}
            phenotypes[sv[4].strip()] = phenotype
    f.close()
    return phenotypes

"""
Read and Store Populations & Individuals
"""
def store_populations(filename):
    f = open(filename,"r",encoding="utf-8")
    for i,line in enumerate(f):
        sv = line.strip().split(";")
        header_list = []
        if i==0:
            header_list = list(map(lambda s: s.replace(".","").replace(" (m)","").replace(" ","_"),sv))
        else:
            pop = Population()
            pop.population_id = sv[0].strip()
            pop.voucher_number = sv[1].strip()
            pop.individuals_sampled = int(sv[4].strip())
            pop.collection_date = datetime.strptime(sv[5].strip(),'%d. %b %y')
            pop.country = sv[6].strip()
            pop.sitename = sv[7].strip()
            pop.location_description = sv[9].strip()
            pop.elevation = int(sv[10].strip())
            pop.latitude = float(sv[11].strip().replace(",","."))
            pop.longitude = float(sv[12].strip().replace(",","."))
            pop.ecology_description = sv[13].strip()
            pop.woody_plant = sv[14].strip()
            #Abundance and Form is missing sv[15]
            pop.pop_size_est = int(sv[16].strip().replace(".",""))
            #Species sv[3]
            try:
                species = Species.objects.get(species=sv[3].strip())
            except:
                species = Species()
                species.species = sv[3].strip()
                species.ncbi_id = TAXONOMY[sv[3].strip()]
                species.save()
            
            pop.species = species
            #Add climate variables
            for j in range(17,len(sv)):
                try:
                    cv = ClimateVariable.objects.get(id=header_list[j])
                except:
                    print("[WARNING]: Climate Variable %s does not exist" % sv[j])
                cvv = ClimateVariableValue(value=float(sv[j].strip()),climate_variable=cv)
            #Add soil variables
            
            pop.save()

            #Individual sv[2]   
            try:
                ind = Individual.objects.get()

    f.close()
