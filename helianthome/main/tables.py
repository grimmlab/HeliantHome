import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe

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
    name = tables.LinkColumn("phenotype_detail",args=[A('id')], verbose_name="Phenotype Name", order_by="name",attrs={"a": {"class": "text-decoration-none"}})
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none"}})
    type = tables.Column(accessor="type", verbose_name="Type")
    category = tables.Column(accessor="category", verbose_name="Category")
    sub_category = tables.Column(accessor="sub_category", verbose_name="Subcategory")
    ontology = tables.Column(accessor="ontology.name", verbose_name="Ontology")
    
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
