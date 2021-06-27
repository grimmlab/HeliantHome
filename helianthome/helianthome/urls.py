"""heliantome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns
#from drf_yasg.views import get_schema_view
#from drf_yasg import openapi

from base import views as base
from main import views as main

import main.rest as rest

'''
schema_view = get_schema_view(
   openapi.Info(
      title="HeliantHOME REST API",
      default_version='v1',
      description="REST API to fetch data from HeliantHOME",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
'''


ID_REGEX = r"[0-9]+"
UUID_REGEX = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$',base.landing_page, name="landing_page"),
    url(r'^about/$',base.about_page, name="about_page"),
    url(r'^download/$',base.download_page, name="download_page"),
    url(r'^faq/$',base.faq_page, name="faq_page"),
    url(r'^species/$',main.species_overview, name="species_overview"),
    url(r'^species/(?P<ncbi_id>[0-9]+)/$',main.species_details, name="species_details"),
    url(r'^populations/$',main.population_overview, name="population_overview"),
    url(r'^population/(?P<population_id>.*)/$',main.population_detail, name="population_detail"),
    url(r'^phenotypes/$',main.phenotype_overview, name="phenotype_overview"),
    url(r'^phenotype/(?P<id>[0-9]+)/$',main.phenotype_detail, name="phenotype_detail"),
    url(r'^individuals/$',main.individuals_overview, name="individuals_overview"),
    url(r'^individual/(?P<individual_id>.*)/$',main.individual_detail, name="individual_detail"),
    url(r'^accessions/$',main.accession_overview, name="accession_overview"),
    url(r'^accession/(?P<accession_id>.*)/$',main.accession_detail, name="accession_detail"),
    url(r'^images/$',main.image_overview, name="image_overview"),

    #url(r'^global-autocomplete/$', GlobalSearchAutocomplete,name='global-autocomplete'),
    #url(r'^search_results/$', base.SearchResults, name="searchresults"),
    #url(r'^search_results//$', base.SearchResults, name="searchresults"),
    #url(r'^search_results/(?P<query>.*)/$', base.SearchResults, name="searchresults"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

restpatterns = [
    #url(r'^rest/api/',  schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^rest/species/list/$', rest.species_list),
    url(r'^rest/species/id/(?P<q>%s)/$' % ID_REGEX, rest.species_detail),
    url(r'^rest/phenotype/list/$', rest.phenotype_list),
    url(r'^rest/phenotype/id/(?P<q>%s)/$' % ID_REGEX, rest.phenotype_detail),
    url(r'^rest/phenotype/id/(?P<q>%s)/values/$' % ID_REGEX, rest.phenotype_value),
    url(r'^rest/population/list/$', rest.population_list),
    url(r'^rest/population/id/(?P<q>%s)/$' % r".*", rest.population_detail),
    url(r'^rest/individual/list/$', rest.individual_list),
    url(r'^rest/individual/id/(?P<q>%s)/$' % r".*", rest.individual_detail),
    url(r'^rest/accession/list/$', rest.accession_list),
    url(r'^rest/accession/id/(?P<q>%s)/$' % r".*", rest.accession_detail),
]

restpatterns = format_suffix_patterns(restpatterns, allowed=['json', 'csv', 'plink', 'zip'])
'''
Add REST patterns to urlpatterns
'''
urlpatterns += restpatterns
