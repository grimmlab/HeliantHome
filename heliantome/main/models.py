from django.db import models

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

    authors = models.ManyToManyField("Author", null=True, blank=True) #author link

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

    species = models.ForeignKey("Species",on_delete=models.CASCADE) #foreign key to species
    publications = models.ManyToManyField("Publication", blank=True)
    update_date = models.DateTimeField(default=None, null=True, blank=True)

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

    def __unicode__(self):
        return u"%s (%s): %s" % (self.species, self.ncbi_id, self.description)

"""
Population model
"""
class Population(models.Model):
    population_id = models.CharField(max_length=20, db_index=True, primary_key=True) #Population ID
    voucher_number = models.CharField(max_length=20, blank=True,null=True) 
    herbarium = models.CharField(max_length=20, blank=True,null=True) 
    individuals_samples = models.IntegerField(blank=True, null=True) #Number of individuals sampled
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

    species = models.ForeignKey("Species",on_delete=models.CASCADE) #foreign key to species
    climate_variables = models.ManyToManyField("ClimateVariable", null=True, blank=True)
    soil_variables = models.ManyToManyField("SoilVariable", null=True, blank=True)

"""
Climate Variables
"""
class ClimateVariable(models.Model):
    short_desc = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    value = models.FloatField()
    
"""
Soil Variables
"""
class SoilVariable(models.Model):
    short_desc = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    value = models.FloatField()
    
"""
Individuals
"""
class Individual(models.Model):
    individual_id = models.CharField(max_length=20, db_index=True,primary_key=True)
    genotype_id = models.CharField(max_length=20, null=True, blank=True)
    
    species = models.ForeignKey("Species",on_delete=models.CASCADE) #foreign key to species
    population = models.ForeignKey("Population",on_delete=models.CASCADE) #foreign key to population


"""
PhenotypeValue model
The indivudal phenotype values. Connected to Phenotype and ObservationUnit
"""
class PhenotypeValue(models.Model):
    value = models.FloatField()
    phenotype = models.ForeignKey('Phenotype',on_delete=models.CASCADE)


"""
Phenotype model
"""
class Phenotype(models.Model):
    name = models.CharField(max_length=255, db_index=True) #phenotype name
    type = models.PositiveSmallIntegerField(choices=PHENOTYPE_TYPE, blank=True, null=True,  db_index=True) #type/category of the phenotype
    description = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True) #how was the scoring of the phenotype done
    category = models.CharField(max_length=255, blank=True,null=True)
    shapiro_test_statistic = models.FloatField(blank=True, null=True) #Shapiro Wilk test for normality
    shapiro_p_value = models.FloatField(blank=True, null=True) #p-value of Shapiro Wilk test
    integration_date = models.DateTimeField(auto_now_add=True) #date of phenotype integration/submission
    #eo_term = models.ForeignKey('OntologyTerm', related_name='eo_term', null=True, blank=True, on_delete=models.CASCADE)
    uo_term = models.ForeignKey('OntologyTerm', related_name='uo_term', null=True, blank=True, on_delete=models.CASCADE)
    to_term = models.ForeignKey('OntologyTerm', related_name='to_term', null=True, blank=True, on_delete=models.CASCADE)
    species = models.ForeignKey('Species', on_delete=models.CASCADE)
    study = models.ForeignKey('Study', on_delete=models.CASCADE)
    population = models.ForeignKey('Population', on_delete=models.CASCADE)

    def get_values_for_acc(self,individual_id):
        """
        Retrieves the phenotype value for a specific accession
        """
        return self.phenotypevalue_set.filter(obs_unit__individual_id=individual_id).values_list("value", flat=True)

    def __unicode__(self):
        if self.to_term is None:
            return u"%s (Phenotype)" % (mark_safe(self.name))
        else:
            return u"%s (Phenotype, TO: %s ( %s ))" % (mark_safe(self.name), mark_safe(self.to_term.name), mark_safe(self.to_term.id))


"""
Image
"""
class PlantImage(models.Model):
    image_id = models.CharField(max_length=255, db_index=True, primary_key=True)
    filename = models.CharField(max_length=255)
    thumb_filename = models.CharField(max_length=255)

    individual = models.ForeignKey("Individual", on_delete=models.CASCADE)


"""
Custom OntologyTerm QuerySet
"""
class OntologyTermQuerySet(models.QuerySet):
    def to_terms(self):
        """Retrieve Trait-Ontology terms."""
        return self.filter(source_id=1)
    def eo_terms(self):
        """Retrieve Environment-Ontology terms."""
        return self.filter(source_id=2)
    def uo_terms(self):
        """Retrieve Unit-Ontology terms."""
        return self.filter(source_id=3)


"""
OntologyTerm model
"""
class OntologyTerm(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    definition = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    source = models.ForeignKey('OntologySource',on_delete=models.CASCADE)
    children = models.ManyToManyField('self', related_name='parents', symmetrical=False)

    objects = OntologyTermQuerySet.as_manager()

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.id)

    def get_info_url(self):
        """return the url for more information about the OntologyTerm"""
        return 'https://bioportal.bioontology.org/ontologies/%s?p=classes&conceptid=http://purl.obolibrary.org/obo/%s' % (self.source.acronym, self.id.replace(':', '_'))



"""
OntologySource model
Type of the ontology (Trait, Environment, etc)
"""
class OntologySource(models.Model):
    acronym = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.acronym)
