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
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
    cultivated = tables.Column(accessor="species.cultivated", verbose_name="Cultivated")
    #individuals_sampled = tables.Column(accessor="individuals_sampled", verbose_name="Individuals Samples")
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
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
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
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
    cultivated = tables.Column(accessor="species.cultivated", verbose_name="Cultivated")
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
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
    individual_id = tables.LinkColumn("individual_detail",args=[A('individual_id')], verbose_name="Individual ID", order_by="individual_id")
    flower = tables.Column(verbose_name="Flower",accessor="plantimage_set")
    leafbottom = tables.Column(verbose_name="Leaf Bottom",accessor="plantimage_set")
    leaftop = tables.Column(verbose_name="Leaf Top",accessor="plantimage_set")
    plantside = tables.Column(verbose_name="Plant Side",accessor="plantimage_set")
    planttop = tables.Column(verbose_name="Plant Top",accessor="plantimage_set")
    primarybranch = tables.Column(verbose_name="Primary Branch",accessor="plantimage_set")
    seed = tables.Column(verbose_name="Seed",accessor="plantimage_set")
    leafstrip = tables.Column(verbose_name="Leaf Strip",accessor="plantimage_set")

    def render_flower(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="flower").thumb_filename +'" style="max-height:80px;width:80px;"></img>')
        except:
            return "-"
    
    def render_leafbottom(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="leafbottom").thumb_filename +'" style="max-height:80px;"></img>')
        except:
            return "-"

    def render_leaftop(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="leaftop").thumb_filename +'" style="max-height:80px;"></img>')
        except:
            return "-"
    
    def render_plantside(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="plantside").thumb_filename +'" style="max-height:80px;"></img>')
        except:
            return "-"
    
    def render_planttop(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="planttop").thumb_filename +'" style="max-height:80px;"></img>')
        except:
            return "-"
    
    def render_primarybranch(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="primarybranch").thumb_filename +'" style="max-height:80px;"></img>')
        except:
            return "-"
    
    def render_seed(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="seed").thumb_filename +'" style="max-height:80px;"></img>')
        except:
            return "-"
    
    def render_leafstrip(self,record):
        try:
            return mark_safe('<img src="' + record.plantimage_set.get(category="leafstrip").thumb_filename +'" style="max-height:80px;"></img>')
        except:
            return "-"

    class Meta:
        attrs = {"class": "table table-striped table-hover"}
        orderable = False

class IndividualPhenotypeTable(tables.Table):
    """
    Display Individual Phenotype Values
    """
    species = tables.LinkColumn("species_details",args=[A('individual__species__ncbi_id')], text=lambda record: record['individual__species__species'], verbose_name="Species", order_by="individual__species__species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
    #id = tables.LinkColumn("phenotype_detail",args=[A('phenotypevalue__phenotype_id')], verbose_name="ID", order_by="phenotypevalue__phenotype_id",attrs={"a": {"class": "text-decoration-none"}},text=lambda record: record['phenotypevalue__phenotype_id'])
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

class AccessionPhenotypeTable(tables.Table):
    """
    Display Accession Phenotype Values
    """
    species = tables.LinkColumn("species_details",args=[A('accession__species__ncbi_id')], text=lambda record: record['accession__species__species'], verbose_name="Species", order_by="accession__species__species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
    #id = tables.LinkColumn("phenotype_detail",args=[A('phenotypevalue__phenotype_id')], verbose_name="ID", order_by="phenotypevalue__phenotype_id",attrs={"a": {"class": "text-decoration-none"}},text=lambda record: record['phenotypevalue__phenotype_id'])
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
    species = tables.LinkColumn("species_details",args=[A('phenotype_link__individual__species__ncbi_id')], text=lambda record: record['phenotype_link__individual__species__species'], verbose_name="Species", order_by="phenotype_link__individual__species__species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
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

class PhenotypeValueTableCultivated(tables.Table):
    """
    Display Phenotype Values for cultivated species
    """
    species = tables.LinkColumn("species_details",args=[A('phenotype_link__accession__species__ncbi_id')], text=lambda record: record['phenotype_link__accession__species__species'], verbose_name="Species", order_by="phenotype_link__accession__species__species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
    population_id = tables.LinkColumn("population_detail",args=[A('phenotype_link__accession__population_id')], verbose_name="Population ID", order_by="phenotype_link__accession__population_id",attrs={"a": {"class": "text-decoration-none"}},text=lambda record: record['phenotype_link__accession__population_id'])
    accession_id = tables.Column(accessor="phenotype_link__accession__accession_id", verbose_name="Accession ID")
    value = tables.Column(accessor="value", verbose_name="Phenotype Value")

    def render_accession_id(self,record):
           return mark_safe('<span class="accession text-decoration-none" style="white-space:nowrap"><a class="text-decoration-none" href="/accession/' + str(record["phenotype_link__accession__accession_id"]) + '/">' + str(record["phenotype_link__accession__accession_id"]) + '</a></span>')
    

    class Meta:
        attrs = {"class": "table table-striped table-hover"}


class AccessionTable(tables.Table):
    """
    Table that is displayed in the accession overview
    """
    accession_id = tables.LinkColumn("accession_detail",args=[A('accession_id')], verbose_name="Individual ID", order_by="accession_id",attrs={"a": {"class": "text-decoration-none"}})
    species = tables.LinkColumn("species_details",args=[A('species.ncbi_id')], text=lambda record: record.species.species, verbose_name="Species", order_by="species.species",attrs={"a": {"class": "text-decoration-none","style":"font-style:italic"}})
    #cultivated = tables.Column(accessor="species__cultivated",verbose_name='Cultivated')
    population = tables.LinkColumn("population_detail",args=[A('population.population_id')], text=lambda record: record.population.population_id, verbose_name="Population", order_by="population.population_id",attrs={"a": {"class": "text-decoration-none"}})
    number_of_phenotypes = tables.Column(accessor="count_phenotypes",verbose_name='# Phenotypes')

    class Meta:
        attrs = {"class": "table table-striped table-hover"}
