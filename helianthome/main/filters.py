from django_filters import rest_framework as filters
from main.models import Population

class PopulationFilter(filters.FilterSet):
    class Meta:
        model = Population
        fields = ('country', 'sitename','species__species')
