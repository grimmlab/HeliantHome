import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe

PHENOTYPE_TYPE = {0:'Quantitative',
                  1:'Categorical',
                  2:'Binary'}

class PopulationTable(tables.Table):
    """
    Table that is displayed in the population overview
    """
    population_id = tables.LinkColumn("population_detail",args=[A('population_id')], verbose_name="Population ID", order_by="population_id",attrs={"a": {"class": "text-decoration-none"}})
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none"}})
    individuals_sampled = tables.Column(accessor="individuals_sampled", verbose_name="Individuals Samples")
    country = tables.Column(accessor="country", verbose_name="Country")
    sitename = tables.Column(accessor="sitename", verbose_name="Sitename")
    elevation = tables.Column(accessor="elevation", verbose_name="Elevation")
    longitude = tables.Column(accessor="longitude", verbose_name="Longitude")
    latitude = tables.Column(accessor="latitude", verbose_name="Latitude")
    pop_size_est = tables.Column(accessor="pop_size_est", verbose_name="Population Size Estimate")
    
    class Meta:
        attrs = {"class": "table table-striped table-hover table-light"}

class IndividualsTable(tables.Table):
    """
    Table that is displayed in the individuals overview
    """
    individual_id = tables.LinkColumn("individual_detail",args=[A('individual_id')], verbose_name="Individual ID", order_by="individual_id",attrs={"a": {"class": "text-decoration-none"}})
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none"}})
    population = tables.LinkColumn("population_detail",args=[A('population.population_id')], text=lambda record: record.population.population_id, verbose_name="Population", order_by="population.population_id",attrs={"a": {"class": "text-decoration-none"}})
    genotype_id = tables.Column(accessor="genotype_id", verbose_name="Genotype ID")
    number_of_phenotypes = tables.Column(accessor="count_phenotypes",verbose_name='# Phenotypes')

    class Meta:
        attrs = {"class": "table table-striped table-hover"}

class PhenotypeTable(tables.Table):
    """
    Table that is displayed in the phenotype overview
    """
    id = tables.LinkColumn("phenotype_detail",args=[A('id')], verbose_name="ID", order_by="id",attrs={"a": {"class": "text-decoration-none"}})
    #name = tables.LinkColumn("phenotype_detail",args=[A('id')], verbose_name="Phenotype Name", order_by="name",attrs={"a": {"class": "text-decoration-none"}})
    name = tables.Column(accessor="name", verbose_name="Phenotype Name")
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none"}})
    type = tables.Column(accessor="type", verbose_name="Type")
    category = tables.Column(accessor="category", verbose_name="Category")
    sub_category = tables.Column(accessor="sub_category", verbose_name="Subcategory")
    ontology = tables.Column(accessor="ontology.name", verbose_name="Ontology")
    
    def render_name(self,record):
        try:
           return mark_safe('<span class="phenotype text-decoration-none" style="white-space:nowrap"><a class="text-decoration-none" href="/phenotype/' + str(record.id) + '/">' + str(record.name) + '</a></span>')
        except:
            return record.name
    
    def render_ontology(self,record):
        try:
           return mark_safe('<span class="fw-lighter text-decoration-none" style="white-space:nowrap"><a class="text-decoration-none" href="' + record.ontology.get_info_url() + '" target="_blank">' + str(record.ontology.name) + ' <i class="bi bi-box-arrow-up-right me-3 fs-6"></i></a></span>')
        except:
            return record.ontology.name

    class Meta:
        attrs = {"class": "table table-striped table-hover"}

class ImageTable(tables.Table):
    """
    Table that is displayed in the image overview
    """
    individual_id = tables.LinkColumn("individual_detail",args=[A('individual.individual_id')], verbose_name="Individual ID", order_by="individual.individual_id")
    species = tables.LinkColumn("species_details",args=[A('individual.species.ncbi_id')], text=lambda record: record.individual.species.species, verbose_name="Species", order_by="individual.species.species")

    class Meta:
        attrs = {"class": "table table-striped table-hover"}

class IndividualPhenotypeTable(tables.Table):
    """
    Display Individual Phenotype Values
    """
    species = tables.LinkColumn("species_details",args=[A('individual__species__ncbi_id')], text=lambda record: record['individual__species__species'], verbose_name="Species", order_by="individual__species__species",attrs={"a": {"class": "text-decoration-none"}})
    id = tables.LinkColumn("phenotype_detail",args=[A('phenotypevalue__phenotype_id')], verbose_name="ID", order_by="phenotypevalue__phenotype_id",attrs={"a": {"class": "text-decoration-none"}},text=lambda record: record['phenotypevalue__phenotype_id'])
    name = tables.LinkColumn("phenotype_detail",args=[A('phenotypevalue__phenotype_id')], verbose_name="Phenotype Name", order_by="phenotypevalue__phenotype__name",attrs={"a": {"class": "text-decoration-none"}}, text=lambda record: record['phenotypevalue__phenotype__name'])
    value = tables.Column(accessor="phenotypevalue__value", verbose_name="Phenotype Value")
    category = tables.Column(accessor="phenotypevalue__phenotype__category", verbose_name="Category")
    sub_category = tables.Column(accessor="phenotypevalue__phenotype__sub_category", verbose_name="Subcategory")
    type = tables.Column(accessor="phenotypevalue__phenotype__type", verbose_name="Type")
    
    def render_type(self,record):
        try:
            return PHENOTYPE_TYPE[record['phenotypevalue__phenotype__type']]
        except:
            return record['phenotypevalue__phenotype__type']

    class Meta:
        attrs = {"class": "table table-striped table-hover"}

class PhenotypeValueTable(tables.Table):
    """
    Display Phenotype Values
    """
    species = tables.LinkColumn("species_details",args=[A('phenotype_link__individual__species__ncbi_id')], text=lambda record: record['phenotype_link__individual__species__species'], verbose_name="Species", order_by="phenotype_link__individual__species__species",attrs={"a": {"class": "text-decoration-none"}})
    population_id = tables.LinkColumn("population_detail",args=[A('phenotype_link__individual__population_id')], verbose_name="Population ID", order_by="phenotype_link__individual__population_id",attrs={"a": {"class": "text-decoration-none"}},text=lambda record: record['phenotype_link__individual__population_id'])
    individual_id = tables.Column(accessor="phenotype_link__individual__individual_id", verbose_name="Individual ID")
    #individual_id = tables.LinkColumn("individual_detail",args=[A('phenotype_link__individual__individual_id')], verbose_name="Individual ID", order_by="phenotype_link__individual__individual_id",attrs={"a": {"class": "text-decoration-none"}},text=lambda record: record['phenotype_link__individual__individual_id'])
    value = tables.Column(accessor="value", verbose_name="Phenotype Value")
    country = tables.Column(accessor="phenotype_link__individual__population__country", verbose_name="Country")
    sitename = tables.Column(accessor="phenotype_link__individual__population__sitename", verbose_name="Sitename")
    latitude = tables.Column(accessor="phenotype_link__individual__population__latitude", verbose_name="Latitude")
    longitude = tables.Column(accessor="phenotype_link__individual__population__longitude", verbose_name="Longitude")

    def render_individual_id(self,record):
           return mark_safe('<span class="individual text-decoration-none" style="white-space:nowrap"><a class="text-decoration-none" href="/individual/' + str(record["phenotype_link__individual__individual_id"]) + '/">' + str(record["phenotype_link__individual__individual_id"]) + '</a></span>')
    

    class Meta:
        attrs = {"class": "table table-striped table-hover"}

