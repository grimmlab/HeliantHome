from django.db import models,connection
from datetime import datetime
import pandas as pd

PHENOTYPE_TYPE = (
    (
        (0, 'Quantitative'),
        (1, 'Categorical'),
        (2, 'Binary')
    )
)

'''
Author Model for Study
'''
class Author(models.Model):
    firstname = models.CharField(max_length=100, blank=True, null=True) #firstname of author
    lastname = models.CharField(max_length=200, blank=True, null=True, db_index=True) #last name of author

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)


'''
Publication Model
'''
class Publication(models.Model):
    author_order = models.TextField() #order of author names
    publication_tag = models.CharField(max_length=255, null=True, blank=True) #publication tag
    pub_year = models.IntegerField(blank=True, null=True) #year of publication
    title = models.CharField(max_length=255, db_index=True) #title of publication
    journal = models.CharField(max_length=255) #journal of puplication
    volume = models.CharField(max_length=255, blank=True, null=True) # volume of publication
    pages = models.CharField(max_length=255, blank=True, null=True) # pages
    doi = models.CharField(max_length=255, db_index=True, blank=True, null=True) #doi
    pubmed_id = models.CharField(max_length=255, db_index=True, blank=True, null=True) #pubmed id

    authors = models.ManyToManyField("Author", blank=True) #author link

    @property
    def author_order_as_list(self):
        return self.author_order.split(",")

    @property
    def pages_as_list(self):
        if self.pages:
            return self.pages.split("-")
        return []

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.title, self.journal, self.pub_year)


"""
Study Model
"""
class Study(models.Model):
    name = models.CharField(max_length=255) #name of study/experiment
    description = models.TextField(blank=True, null=True) #short study description

    publications = models.ManyToManyField("Publication", blank=True)
    update_date = models.DateTimeField(default=None, null=True, blank=True)

    def value_as_dataframe(self,sam=False):
        """
        Returns the PhenotypValue records for this study as a pandas dataframe
        """
        cursor = connection.cursor()
        if sam:
            cursor.execute("""
                    SELECT v.id,o.accession_id,po.population_id as population_id,s.species,p.id as phenotype_id, p.name as phenotype_name, v.value
                    FROM main_phenotypevalue as v
                    LEFT JOIN main_phenotypelink o ON v.phenotype_link_id = o.id
                    LEFT JOIN main_phenotype as p ON p.id = v.phenotype_id
                    LEFT JOIN main_accession as a ON a.accession_id = o.accession_id
                    LEFT JOIN main_population as po ON po.population_id = a.population_id
                    LEFT JOIN main_species as s ON s.id = a.species_id
                    WHERE p.study_id = %s ORDER BY o.accession_id,p.id ASC """ % self.id)
            data = pd.DataFrame(cursor.fetchall(),
                                columns=['id', 'accession_id', 'population_id',
                                         'species', 'phenotype_id', 'phenotype_name',
                                         'value']).set_index(['id'])

        else:
            cursor.execute("""
                    SELECT v.id,o.individual_id,po.population_id as population_id,s.species,p.id as phenotype_id, p.name as phenotype_name, v.value
                    FROM main_phenotypevalue as v
                    LEFT JOIN main_phenotypelink o ON v.phenotype_link_id = o.id
                    LEFT JOIN main_phenotype as p ON p.id = v.phenotype_id
                    LEFT JOIN main_individual as a ON a.individual_id = o.individual_id
                    LEFT JOIN main_population as po ON po.population_id = a.population_id
                    LEFT JOIN main_species as s ON s.id = a.species_id
                    WHERE p.study_id = %s ORDER BY o.individual_id,p.id ASC """ % self.id)
            data = pd.DataFrame(cursor.fetchall(),
                                columns=['id', 'individual_id', 'population_id',
                                         'species', 'phenotype_id', 'phenotype_name',
                                         'value']).set_index(['id'])
        return data

    def get_matrix_and_accession_map(self, sam=False,column='phenotype_name'):
        """Returns both the dataframe and a matrix version of it"""
        if sam:
            data = self.value_as_dataframe(sam=sam)
            data.set_index(['accession_id'], inplace=True)
            df_pivot = data.pivot(columns=column, values='value')
            data.drop(['value', 'phenotype_id', 'phenotype_name'], axis=1, inplace=True)
            data = data[~data.index.duplicated(keep='first')]
        else:
            data = self.value_as_dataframe(sam=sam)
            data.set_index(['individual_id'], inplace=True)
            df_pivot = data.pivot(columns=column, values='value')
            data.drop(['value', 'phenotype_id', 'phenotype_name'], axis=1, inplace=True)
            data = data[~data.index.duplicated(keep='first')]
        return (data, df_pivot)

    @property
    def count_phenotypes(self):
        """Returns number of phenotypes"""
        return self.phenotype_set.count()

    def save(self, *args, **kwargs):
        self.update_date = datetime.now()
        super(Study, self).save(*args, **kwargs)

    @property
    def name_link(self):
        """Returns the name with empty string replaced by underscore"""
        return self.name.replace(" ","_")

    def __unicode__(self):
        return u"%s (Study)" % (mark_safe(self.name))

"""
Species model
"""
class Species(models.Model):
    ncbi_id = models.IntegerField(blank=True, null=True) #NCBI Taxonomy ID
    species = models.CharField(max_length=255) #Species name
    description = models.TextField(blank=True, null=True) #short species description
    species_image = models.CharField(max_length=255, blank=True,null=True) #Species image
    cultivated = models.BooleanField(default=False) #is species cultivated or not
    
    study = models.ForeignKey("Study",blank=True,null=True,on_delete=models.CASCADE) #foreign key to species

    def __unicode__(self):
        return u"%s (%s): %s" % (self.species, self.ncbi_id, self.description)

"""
Climate Variables
"""
class ClimateVariable(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
    description = models.CharField(max_length=255)

"""
Climate Variable Value
"""
class ClimateVariableValue(models.Model):
    value = models.FloatField()
    climate_variable = models.ForeignKey("ClimateVariable",on_delete=models.CASCADE)

"""
Soil Variables
"""
class SoilVariable(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
    description = models.CharField(max_length=255)

"""
Soil Variable Value
"""
class SoilVariableValue(models.Model):
    value = models.FloatField()
    soil_variable = models.ForeignKey("SoilVariable",on_delete=models.CASCADE)
    

"""
Population model
"""
class Population(models.Model):
    population_id = models.CharField(max_length=20, db_index=True, primary_key=True) #Population ID
    voucher_number = models.CharField(max_length=20, blank=True,null=True) 
    herbarium = models.CharField(max_length=20, blank=True,null=True) 
    individuals_sampled = models.IntegerField(blank=True, null=True) #Number of individuals sampled
    collection_date = models.DateTimeField(null=True, blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    sitename = models.TextField(blank=True, null=True) #name of site if available
    elevation = models.IntegerField(blank=True, null=True)
    longitude = models.FloatField(null=True, blank=True, db_index=True) #longitude of accession
    latitude = models.FloatField(null=True, blank=True, db_index=True) #latitude of accession
    location_description = models.TextField(blank=True, null=True)
    ecology_description = models.TextField(blank=True, null=True) 
    woody_plant = models.TextField(blank=True, null=True) #Major associated woody plant genera
    pop_size_est = models.IntegerField(blank=True, null=True) #population size estimate

    species = models.ForeignKey("Species",blank=True,null=True,on_delete=models.CASCADE) #foreign key to species
    climate_variables = models.ManyToManyField("ClimateVariableValue",  blank=True)
    soil_variables = models.ManyToManyField("SoilVariableValue",  blank=True)
    
    def value_as_dataframe(self):
        """
        Returns the PhenotypValue records for this population as a pandas dataframe
        """
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT v.id,o.individual_id,po.population_id as population_id,s.species,p.id as phenotype_id, p.name as phenotype_name, v.value
                    FROM main_phenotypevalue as v
                    LEFT JOIN main_phenotypelink o ON v.phenotype_link_id = o.id
                    LEFT JOIN main_phenotype as p ON p.id = v.phenotype_id
                    LEFT JOIN main_individual as a ON a.individual_id = o.individual_id
                    LEFT JOIN main_population as po ON po.population_id = a.population_id
                    LEFT JOIN main_species as s ON s.id = a.species_id
                    WHERE po.population_id = '%s' ORDER BY o.individual_id,p.id ASC """ % self.population_id)
        data = pd.DataFrame(cursor.fetchall(),
                            columns=['id', 'individual_id', 'population_id',
                                         'species', 'phenotype_id', 'phenotype_name',
                                         'value']).set_index(['id'])
        return data

    def get_matrix_and_accession_map(self, column='phenotype_name'):
        """Returns both the dataframe and a matrix version of it"""
        data = self.value_as_dataframe()
        data.set_index(['individual_id'], inplace=True)
        df_pivot = data.pivot(columns=column, values='value')
        data.drop(['value', 'phenotype_id', 'phenotype_name'], axis=1, inplace=True)
        data = data[~data.index.duplicated(keep='first')]
        return (data, df_pivot)



"""
Individuals
"""
class Individual(models.Model):
    individual_id = models.CharField(max_length=20, db_index=True,primary_key=True)
    genotype_id = models.CharField(max_length=20, null=True, blank=True)
    
    species = models.ForeignKey("Species",blank=True,null=True,on_delete=models.CASCADE) #foreign key to species
    population = models.ForeignKey("Population",blank=True,null=True,on_delete=models.CASCADE) #foreign key to population

"""
Accessions
"""
class Accession(models.Model):
    accession_id = models.CharField(max_length=20, db_index=True,primary_key=True)
    ppn = models.CharField(max_length=20, db_index=True,blank=True,null=True)
    pit = models.CharField(max_length=20, db_index=True,blank=True,null=True)
    aclass = models.CharField(max_length=20, db_index=True,blank=True,null=True)
    name = models.CharField(max_length=20, db_index=True,blank=True,null=True)
    
    species = models.ForeignKey("Species",blank=True,null=True,on_delete=models.CASCADE) #foreign key to species
    population = models.ForeignKey("Population",blank=True,null=True,on_delete=models.CASCADE) #foreign key to population


"""
PhenotypeLink model
Link Phenotype Values to Individuals
"""
class PhenotypeLink(models.Model):
    individual = models.ForeignKey('Individual',blank=True,null=True,on_delete=models.CASCADE)
    accession = models.ForeignKey('Accession',blank=True,null=True,on_delete=models.CASCADE)
    study = models.ForeignKey('Study',blank=True,null=True,on_delete=models.CASCADE)

"""
PhenotypeValue model
The indivudal phenotype values. Connected to Phenotype and ObservationUnit
"""
class PhenotypeValue(models.Model):
    value = models.FloatField()
    phenotype = models.ForeignKey('Phenotype',on_delete=models.CASCADE)
    phenotype_link = models.ForeignKey('PhenotypeLink',blank=True,null=True,on_delete=models.CASCADE)


"""
Phenotype model
"""
class Phenotype(models.Model):
    name = models.CharField(max_length=255, db_index=True) #phenotype name
    type = models.PositiveSmallIntegerField(choices=PHENOTYPE_TYPE, blank=True, null=True,  db_index=True) #type/category of the phenotype
    description = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True) #how was the scoring of the phenotype done
    unit = models.TextField(blank=True, null=True) #how was the scoring of the phenotype done
    category = models.CharField(max_length=255, blank=True,null=True)
    sub_category = models.CharField(max_length=255, blank=True,null=True)
    shapiro_test_statistic = models.FloatField(blank=True, null=True) #Shapiro Wilk test for normality
    shapiro_p_value = models.FloatField(blank=True, null=True) #p-value of Shapiro Wilk test
    integration_date = models.DateTimeField(auto_now_add=True) #date of phenotype integration/submission
    ontology = models.ForeignKey('OntologyTerm', null=True, blank=True, on_delete=models.CASCADE)
    
    easygwas_link = models.CharField(max_length=500, blank=True,null=True)
    
    species = models.ForeignKey('Species',blank=True,null=True, on_delete=models.CASCADE)
    study = models.ForeignKey('Study',blank=True, null=True,on_delete=models.CASCADE)

    def get_values_for_ind(self,individual_id):
        """
        Retrieves the phenotype value for a specific individual
        """
        return self.phenotypevalue_set.filter(phenotype_link__individual=individual_id).values_list("value", flat=True)
    
    def get_values_for_acc(self,accession_id):
        """
        Retrieves the phenotype value for a specific individual
        """
        return self.phenotypevalue_set.filter(phenotype_link__accession=accession_id).values_list("value", flat=True)


    def __unicode__(self):
        if self.to_term is None:
            return u"%s (Phenotype)" % (mark_safe(self.name))
        else:
            return u"%s (Phenotype, TO: %s ( %s ))" % (mark_safe(self.name), mark_safe(self.ontology.name), mark_safe(self.ontology.id))


"""
Image
"""
class PlantImage(models.Model):
    category = models.CharField(max_length=255)
    thumb_filename = models.CharField(max_length=255)

    description = models.CharField(max_length=500)

    individual = models.ForeignKey("Individual",blank=True,null=True, on_delete=models.CASCADE)
    accession = models.ForeignKey("Accession",blank=True,null=True, on_delete=models.CASCADE)
    study = models.ForeignKey('Study',blank=True, null=True,on_delete=models.CASCADE)


"""
OntologyTerm model
"""
class OntologyTerm(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.id)
    
    def get_info_url(self):
        """return the url for more information about the OntologyTerm"""
        return 'https://bioportal.bioontology.org/ontologies/PTO?p=classes&conceptid=http://purl.obolibrary.org/obo/%s' % self.id


