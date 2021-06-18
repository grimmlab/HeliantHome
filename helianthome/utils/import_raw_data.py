import h5py
import numpy as np
import os
from main.models import *
from datetime import datetime

TAXONOMY = {"Helianthus annuus":4232,
            "Helianthus argophyllus":73275,
            "Helianthus annuus subsp. texanus":1312900,
            "Helianthus petiolaris subsp. fallax":74150,
            "Helianthus petiolaris subsp. petiolaris":74151,
            "Helianthus niveus subsp. canescens":74145,
            "Helianthus annuus var. macrocarpus":0}

CULTIVATED = {"Helianthus annuus":0,
            "Helianthus argophyllus":0,
            "Helianthus annuus subsp. texanus":0,
            "Helianthus petiolaris subsp. fallax":0,
            "Helianthus petiolaris subsp. petiolaris":0,
            "Helianthus niveus subsp. canescens":0,
            "Helianthus annuus var. macrocarpus":1}

SPECIES_IMAGES = {"Helianthus annuus":"/media/images/species/helianthus_annuus.jpg",
                  "Helianthus argophyllus":"/media/images/species/helianthus_argophyllus.jpg",
                  "Helianthus annuus subsp. texanus":"/media/images/species/helianthus_annuus_subsp_texanus.jpg",
                  "Helianthus petiolaris subsp. fallax":"/media/images/species/helianthus_petiolaris_subsp_fallax.jpg",
                  "Helianthus petiolaris subsp. petiolaris":"/media/images/species/helianthus_petiolaris_subsp_petiolaris.jpg",
                  "Helianthus niveus subsp. canescens":"/media/images/species/helianthus_niveus_subsp_canescens.jpg",
                  "Helianthus annuus var. macrocarpus":""}

SPECIES_DESCRIPTION = {"Helianthus annuus":'It’s an annual plant frequently found between the southern Canada and all across the western US until the north of Mexico. It is the most widely distributed species of Helianthus and the closest relative to the cultivated sunflower. Members of the species show a broad range of variation in plant size (up to 4 meters tall), architecture, Inflorescences and pigmentation. At the same time, they can be found in all kind of environments, growing from sea level to 2,500 m both in low and moderate rainfall areas (<a href="http://doi.wiley.com/10.2134/agronmonogr19.c2">Heiser et al. 1978</a>).',
                  "Helianthus argophyllus":'Also known as the Silverleaf sunflower, is an annual plant native to the coastal regions of Texas, in the US.<br>The full grown plant can reach up to 3 m tall. Its leaves are ovate and densely covered with long silky hairs as well as the stem. The flowerheads are about 3 cm of diameter with yellow ligules on ray flowers (<a href="http://doi.wiley.com/10.2134/agronmonogr19.c2">Heiser et al. 1978</a>).',
                  "Helianthus annuus subsp. texanus":'',
                  "Helianthus petiolaris subsp. fallax":'Commonly known as the prairie sunflower, it’s an annual species with a height that goes from 0.4 to 2.0 m tall, usually very branched This species is widely distributed across the west and central US and comprises two morphological races: <em><a href="/species/74151/" target="_blank">subsp. petiolaris</a></em> of the Great Plains and <em><a href="/species/74150/" target="_blank">subsp. fallax</a></em> Heiser of the Southwest (<a target="_blank" href="http://doi.wiley.com/10.2134/agronmonogr19.c2">Heiser et al. 1978</a>).',
                  "Helianthus petiolaris subsp. petiolaris":'Commonly known as the prairie sunflower, it’s an annual species with a height that goes from 0.4 to 2.0 m tall, usually very branched This species is widely distributed across the west and central US and comprises two morphological races: <em><a href="/species/74151/" target="_blank">subsp. petiolaris</a></em> of the Great Plains and <em><a href="/species/74150/" target="_blank">subsp. fallax</a></em> Heiser of the Southwest (<a target="_blank" href="http://doi.wiley.com/10.2134/agronmonogr19.c2">Heiser et al. 1978</a>).',
                  "Helianthus niveus subsp. canescens":'Also known as Grey Sunflower, mostly annual plants, smaller than other species with individuals of 50 to 150 cm tall. Extremely branched with small inflorescences. Found in Mexico (Sonora) , and in the US (Arizona and California).',
                  "Helianthus annuus var. macrocarpus":'Commonly known as cultivated sunflower, it’s a variety nested within the H.annuus species, shorter than most of it’s wild relatives, with large single flowerheads, most of the times not branched.'}

"""
Read and Store Climate Variables
"""
def store_climate_variables(filename="../data/climate_variables.csv"):
    f = open(filename,"r",encoding="utf-8")
    for i,line in enumerate(f):
        if i!=0:
            sv = line.strip().split(";")
            cv = ClimateVariable(name=sv[0].strip(),description=sv[1].strip())
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
            cv = SoilVariable(name=sv[0].strip(),description=sv[1].strip())
            cv.save()
    f.close()
    print("Stored Soil Variables")


"""
Read and Store Populations & Individuals
"""
def store_populations(filename):
    f = open(filename,"r",encoding="utf-8")
    for i,line in enumerate(f):
        sv = line.strip().split(";")
        if i==0:
            header_list = list(map(lambda s: s.replace(".","").replace(" (m)","").replace(" ","_"),sv))
        else:
            pop = Population()
            pop.population_id = sv[0].strip()
            pop.voucher_number = sv[1].strip()
            pop.voucher_number = sv[2].strip()
            pop.individuals_sampled = int(sv[5].strip())
            pop.collection_date = datetime.strptime(sv[6].strip(),'%d. %b %y')
            pop.country = sv[7].strip()
            pop.sitename = sv[8].strip()
            pop.location_description = sv[10].strip()
            pop.elevation = int(sv[11].strip())
            pop.latitude = float(sv[12].strip().replace(",","."))
            pop.longitude = float(sv[13].strip().replace(",","."))
            pop.ecology_description = sv[14].strip()
            pop.woody_plant = sv[15].strip()
            #Abundance and Form is missing sv[16]
            pop.pop_size_est = int(sv[17].strip().replace(".",""))
            #Species sv[3]
            try:
                species = Species.objects.get(species=sv[4].strip())
            except:
                species = Species()
                species.species = sv[4].strip()
                species.ncbi_id = TAXONOMY[sv[4].strip()]
                species.species_image = SPECIES_IMAGES[sv[4].strip()]
                species.save()
            pop.species = species
            #Save Model   
            pop.save()
            
            #Add climate & soil variables
            for j in range(18,len(sv)):
                val = sv[j].strip().replace(",",".")
                if val=="NA":
                    val = np.nan
                else:
                    val = float(val)
                    try:
                        cv = ClimateVariable.objects.get(name=header_list[j])
                        cvv = ClimateVariableValue(value=val,climate_variable=cv)
                        cvv.save()
                        pop.climate_variables.add(cvv)
                    except:
                        cv = SoilVariable.objects.get(name=header_list[j])
                        cvv = SoilVariableValue(value=val,soil_variable=cv)
                        cvv.save()
                        pop.soil_variables.add(cvv)

            #Individual sv[3]
            idvv = sv[3].strip().split(",")
            for idv1 in idvv:
                idv = idv1.strip().split("-")
                start = int(idv[0][-4:])
                if len(idv)==1:
                    end = start+1
                else:
                    end = int(idv[1])+1
                for i in range(end-start):
                    ind_id = idv[0][:3] + f'{start+i:04d}'
                    try:
                        ind = Individual.objects.get(individual_id=ind_id)
                        print("[Warning]: Species already exists and linked to Population: %s" % ind_id)
                    except:
                        ind = Individual(individual_id=ind_id,species=species,population=pop)
                        ind.save()
    f.close()
    print("[Done]: Stored Populations successfully")

"""
Load Phenotype Descriptions
"""
def load_phenotype_descriptions(filename="../data/phenotype_description.csv"):
    f = open(filename,"r",encoding="latin-1")
    phenotypes = {}
    for i,line in enumerate(f):
        if i!=0:
            sv = line.strip().split("\t")
            phenotype = {'category':sv[0].strip(),
                         'sub_category':sv[1].strip(),
                         'ontology_name':sv[2].strip(),
                         'ontology_id':sv[3].strip().split("/")[-1],
                         'name':sv[4].strip(),
                         'unit':sv[5].strip(),
                         'description':sv[6].strip(),
                         'method':sv[7].strip(),
                         'image':sv[8].strip(),
                         'type':int(sv[9].strip())}
            phenotypes[sv[4].strip()] = phenotype
    f.close()
    return phenotypes

def store_phenotype_values(filename):
    pd = load_phenotype_descriptions("../data/phenotype_description.csv")
    phenotypes = {}
    f = open(filename,"r",encoding="utf-8")
    for i,line in enumerate(f):
        sv = line.strip().split(";")
        if i==0:
            for j in range(2,len(sv)):
                pn = sv[j].strip().replace(" ","_")
                if pn in pd:
                    p = pd[pn]
                    pheno = Phenotype()
                    pheno.name = pn.remove("_"," ")
                    pheno.type = p['type']
                    pheno.description = p['description']
                    pheno.method = p['method']
                    pheno.category = p['category']
                    pheno.sub_category = p['sub_category']
                    try:
                        ontology = OntologyTerm.objects.get(id=p['ontology_id'])
                    except:
                        ontology = OntologyTerm()
                        ontology.id = p['ontology_id']
                        ontology.name = p['ontology_name']
                        ontology.save()
                    pheno.ontology = ontology
                    pheno.save()
                    phenotypes[j] = pheno
                else:
                    print("ERROR PHENOTYPE IS NOT IN LIST: %s" % pn)
                    quit()
        else:
            #try:
                ind = Individual.objects.get(individual_id=sv[0].strip())
                ind.genotype_id = sv[1].strip()
                ind.save()
                for j in range(2,len(sv)):
                    pheno = phenotypes[j]
                    if i==1:#update species name
                        pheno.species = ind.species
                        pheno.save()  
                    
                    val = sv[j].strip().replace(",",".")
                    if val=="NA":
                        val = np.nan
                    else:
                        pv = PhenotypeValue()
                        val = float(val)
                        pl = PhenotypeLink()
                        pl.individual = ind
                        #pl.study = 
                        pl.save()
                        pv.value = val
                        pv.phenotype = pheno
                        pv.phenotype_link = pl
                        pv.save()
            #except:
            #    print("[ERROR STORE PHENOTYPE]: Individual ID %s does not exist." % sv[0])
            #    quit()
    f.close()
    print("Successfully stored %s phenotypes" % filename)

def store_images(filename):
    f = open(filename,"r",encoding="utf-8")
    media = "/media/images/thumbnails/"
    for i,line in enumerate(f):
        if i!=0:
            sv = line.strip().split(",")
            ind = Individual.objects.get(individual_id=sv[0].strip())
            for img in sv[1:]:
                if img.strip()=="nan":
                    continue
                elif img.strip().split("_")[-1]=="flower":
                    pimg = PlantImage(category="flower",thumb_filename=os.path.join(media,os.path.join("flower",img.strip() + ".jpg")),
                                      individual=ind, description="High Resolution Image of individual sunflower inflorescences showing both top and bottom sides of them (most of the times in triplicate).")
                    pimg.save()
                elif img.strip().split("_")[-1]=="leafbottom":
                    pimg = PlantImage(category="leafbottom",thumb_filename=os.path.join(media,os.path.join("leafbottom",img.strip() + ".jpg")),
                                     individual=ind, description="300 dpi resolution image of individual sunflower leaf (abaxial)")
                    pimg.save()
                elif img.strip().split("_")[-1]=="leaftop":
                    pimg = PlantImage(category="leaftop",thumb_filename=os.path.join(media,os.path.join("leaftop",img.strip() + ".jpg")),
                                      individual=ind,description="300 dpi resolution image of sunflower leaf of each studied individual (adaxial)")
                    pimg.save()
                elif img.strip().split("_")[-1]=="plantside":
                    pimg = PlantImage(category="plantside",thumb_filename=os.path.join(media,os.path.join("plantside",img.strip() + ".jpg")),
                                      indivaidual=ind,description="High resolution image of sunflower whole plant of each studied individual (side view)")
                    pimg.save()
                elif img.strip().split("_")[-1]=="planttop":
                    pimg = PlantImage(category="planttop",thumb_filename=os.path.join(media,os.path.join("planttop",img.strip() + ".jpg")),
                                      individual=ind,description="High resolution image of sunflower whole plant of each studied individual (top view)")
                    pimg.save()
                elif img.strip().split("_")[-1]=="primarybranch":
                    pimg = PlantImage(category="primarybranch",thumb_filename=os.path.join(media,os.path.join("primarybranch",img.strip() + ".jpg")),
                                      individual=ind,description="High resolution image of branch sections of each studied individual (about 8 com long) cut from their primary branch.")
                    pimg.save()
                elif img.strip().split("_")[-1]=="seed":
                    pimg = PlantImage(category="seed",thumb_filename=os.path.join(media,os.path.join("seed",img.strip() + ".jpg")),
                                      individual=ind,description="High resolution image of branch sections of each studied individual (about 8 com long) cut from their primary branch.")
                    pimg.save()
                elif img.strip().split("_")[-1]=="leafstrip":
                    pimg = PlantImage(category="leafstrip",thumb_filename=os.path.join(media,os.path.join("leafstrip",img.strip() + ".jpg")),
                                      individual=ind,description="High Resolution Image (2400 dpi) of sunflower leaf sections for each studied individual.")
                    pimg.save()
    f.close()
    print("Successfully stored %s thumbnails" % filename)

def integrate():
    store_climate_variables(filename="../data/climate_variables.csv")
    store_soil_variables(filename="../data/soil_variables.csv")
    store_populations(filename="../data/populations.csv")
    store_phenotype_values(filename="../data/phenotypes_h_annuus.csv")
    store_phenotype_values(filename="../data/phenotypes_h_argophyllus.csv")
    store_phenotype_values(filename="../data/phenotypes_h_n_canescens.csv")
    store_phenotype_values(filename="../data/phenotypes_h_p_fallax.csv")
    store_phenotype_values(filename="../data/phenotypes_h_p_petiolaris.csv")
    store_images(filename="../data/thumbnails.txt")
