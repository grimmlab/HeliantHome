
from rest_framework import serializers

from main.models import Phenotype,PhenotypeValue
from main.models import PHENOTYPE_TYPE

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


