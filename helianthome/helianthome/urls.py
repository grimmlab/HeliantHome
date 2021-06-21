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

from base import views as base
from main import views as main

from base.autocomplete_light_registry import GlobalSearchAutocomplete

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$',base.landing_page, name="landing_page"),
    url(r'^about/$',base.about_page, name="about_page"),
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

    url(r'^global-autocomplete/$', GlobalSearchAutocomplete,name='global-autocomplete'),
    #url(r'^search_results/$', base.SearchResults, name="searchresults"),
    #url(r'^search_results//$', base.SearchResults, name="searchresults"),
    #url(r'^search_results/(?P<query>.*)/$', base.SearchResults, name="searchresults"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

