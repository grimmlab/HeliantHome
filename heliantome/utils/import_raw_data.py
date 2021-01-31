import h5py
import numpy as np
from main.models import ClimateVariable, SoilVariable

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
Read and Store Phenotype Descriptions
"""
def store_phenotype_descriptions(filename):
    f = open(filename,"r",encoding="utf-8")
    for i,line in enumerate(f):
        if i!=0:
            sv = line.strip().split(";")
            print(sv)
    f.close()

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
            for elem in sv:
                pass
    f.close()
