import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe

class PopulationTable(tables.Table):
    """
    Table that is displayed in the population overview
    """
    population_id = tables.LinkColumn("population_detail",args=[A('population_id')], verbose_name="Population ID", order_by="population_id")
    species = tables.Column(accessor="species.species", verbose_name="Species")
    individuals_sampled = tables.Column(accessor="individuals_sampled", verbose_name="Individuals Samples")
    country = tables.Column(accessor="country", verbose_name="Country")
    sitename = tables.Column(accessor="sitename", verbose_name="Sitename")
    elevation = tables.Column(accessor="elevation", verbose_name="Elevation")
    longitude = tables.Column(accessor="longitude", verbose_name="Longitude")
    latitude = tables.Column(accessor="latitude", verbose_name="Latitude")
    pop_size_est = tables.Column(accessor="pop_size_est", verbose_name="Population Size Estimate")

    class Meta:
        attrs = {"class": "table table-striped table-hover"}
