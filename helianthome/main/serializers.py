
from rest_framework import serializers

from main.models import Phenotype,PhenotypeValue
from main.models import Species,Population
from main.models import ClimateVariableValue, SoilVariableValue
from main.models import PHENOTYPE_TYPE
from main.models import Individual, Accession

'''
Species List Serializer Class
'''
class SpeciesListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cultivated = serializers.SerializerMethodField()
    
    class Meta:
        model = Species
        exclude = ('species_image',)

    def get_id(self,obj):
        return obj.ncbi_id
    
    def get_species(self,obj):
        return obj.species
    
    def get_description(self,obj):
        return obj.description
    
    def get_cultivated(self,obj):
        return obj.cultivated

    

'''
Phenotype List Serializer Class (read-only: might be extended to also allow integration of new data)
'''
class PhenotypeListSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField()
    phenotype_id = serializers.SerializerMethodField()
    phenotype_name = serializers.SerializerMethodField()
    num_values = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    method = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    easygwas_link = serializers.SerializerMethodField()
    ontology_name = serializers.SerializerMethodField()
    ontology_id = serializers.SerializerMethodField()


    class Meta:
        model = Phenotype
        exclude = ('shapiro_test_statistic','shapiro_p_value','integration_date')
    
    def get_species(self,obj):
        return obj.species.species

    def get_phenotype_id(self,obj):
        return obj.id
    
    def get_phenotype_name(self,obj):
        return obj.name

    def get_num_values(self, obj):
        try:
            return obj.phenotypevalue_set.count()
        except:
            return ""
    
    def get_description(self, obj):
        try:
            return obj.description
        except:
            return ""
    
    def get_method(self, obj):
        try:
            return obj.method
        except:
            return ""

    def get_category(self, obj):
        try:
            return obj.category
        except:
            return ""
    
    def get_subcategory(self, obj):
        try:
            return obj.sub_category
        except:
            return ""
    
    def get_type(self, obj):
        try:
            return PHENOTYPE_TYPE[obj.type]
        except:
            return ""
    
    def get_easygwas_link(self, obj):
        try:
            return obj.easygwas_link
        except:
            return ""
    
    def get_ontology_name(self, obj):
        try:
            return obj.ontology.name
        except:
            return ""
    
    def get_ontology_id(self, obj):
        try:
            return obj.ontology.id
        except:
            return ""

'''
Phenotype Individual Value Serializer Class
'''
class PhenotypeValueSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField()
    phenotype_id = serializers.SerializerMethodField()
    phenotype_name = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    phenotype_value = serializers.SerializerMethodField()

    class Meta:
        model = PhenotypeValue
        fields = ('species','phenotype_id','phenotype_name','population','id',
                  'phenotype_value')

    def get_species(self,obj):
        try:
            return obj.phenotype.species.species
        except:
            return ""
    
    def get_phenotype_id(self,obj):
        try:
            return obj.phenotype.id
        except:
            return ""

    def get_phenotype_name(self,obj):
        try:
            return obj.phenotype.name
        except:
            return ""

    def get_population(self,obj):
        try:
            try:
                return obj.phenotype_link.individual.population.population_id
            except:
                return obj.phenotype_link.accession.population.population_id
        except:
            return ""
    
    def get_id(self,obj):
        try:
            try:
                return obj.phenotype_link.individual.individual_id
            except:
                return obj.phenotype_link.accession.accession_id
        except:
            return ""

    def get_phenotype_value(self,obj):
        try:
            return obj.value
        except:
            return ""

'''
Climate Variable Serializer Class
'''
class ClimateVariableSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = ClimateVariableValue
        fields = ('name','value','description')

    def get_name(self,obj):
        return obj.climate_variable.name
    
    def get_value(self,obj):
        return obj.value
    
    def get_description(self,obj):
        return obj.climate_variable.description

'''
Soil Variable Serializer Class
'''
class SoilVariableSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = SoilVariableValue
        fields = ('name','value','description')

    def get_name(self,obj):
        return obj.soil_variable.name
    
    def get_value(self,obj):
        return obj.value
    
    def get_description(self,obj):
        return obj.soil_variable.description

'''
Population List Serializer Class
'''
class PopulationListSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField()
    population_id = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    sitename = serializers.SerializerMethodField()
    location_description = serializers.SerializerMethodField()
    elevation = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    #climate_variables = ClimateVariableSerializer(source='climate_variables', many=True)
    #soil_variables = SoilVariableSerializer(source='soil_variables', many=True)
    climate_variables = ClimateVariableSerializer(many=True)
    soil_variables = SoilVariableSerializer(many=True)

    class Meta:
        model = Population
        exclude = ('herbarium','voucher_number','individuals_sampled',
                   'collection_date','woody_plant','pop_size_est')

    
    def get_species(self,obj):
        return obj.species.species
    
    def get_population_id(self,obj):
        return obj.population_id
    
    def get_country(self,obj):
        return obj.country
    
    def get_sitename(self,obj):
        return obj.sitename
    
    def get_location_description(self,obj):
        return obj.location_description
    
    def get_elevation(self,obj):
        return obj.elevation
    
    def get_latitude(self,obj):
        return obj.latitude
    
    def get_longitude(self,obj):
        return obj.longitude
    
    def get_description(self,obj):
        return obj.ecology_description
    
'''
Individual List Serializer Class
'''
class IndividualListSerializer(serializers.ModelSerializer):
    individual_id = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    population_id = serializers.SerializerMethodField()
    genotype_id = serializers.SerializerMethodField()
    num_phenotypes = serializers.SerializerMethodField()
    
    class Meta:
        model = Individual
        fields = ('individual_id','species','population_id',
                  'genotype_id','num_phenotypes')

    def get_individual_id(self,obj):
        return obj.individual_id
    
    def get_species(self,obj):
        return obj.species.species
    
    def get_population_id(self,obj):
        return obj.population.population_id
    
    def get_genotype_id(self,obj):
        return obj.genotype_id
    
    def get_num_phenotypes(self,obj):
        return obj.phenotypelink_set.count()

'''
Accession List Serializer Class
'''
class AccessionListSerializer(serializers.ModelSerializer):
    accession_id = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    population_id = serializers.SerializerMethodField()
    planting_packet_number = serializers.SerializerMethodField()
    pit_name = serializers.SerializerMethodField()
    line_class = serializers.SerializerMethodField()
    line_name = serializers.SerializerMethodField()
    num_phenotypes = serializers.SerializerMethodField()
    
    class Meta:
        model = Accession
        fields = ('accession_id','species','population_id',
                  'planting_packet_number','pit_name','line_class',
                  'line_name','num_phenotypes')

    def get_accession_id(self,obj):
        return obj.accession_id
    
    def get_species(self,obj):
        return obj.species.species
    
    def get_population_id(self,obj):
        return obj.population.population_id
    
    def get_planting_packet_number(self,obj):
        return obj.ppn
    
    def get_pit_name(self,obj):
        return obj.pit
    
    def get_line_class(self,obj):
        return obj.aclass
    
    def get_line_name(self,obj):
        return obj.name
    
    def get_num_phenotypes(self,obj):
        return obj.phenotypelink_set.count()
