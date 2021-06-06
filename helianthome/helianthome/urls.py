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

from base import views as base
from main import views as main


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',base.landing_page, name="landing_page"),
    url(r'^about/',base.about_page, name="about_page"),
    url(r'^species/$',main.species_overview, name="species_overview"),
    url(r'^species/(?P<ncbi_id>[0-9]+)/$',main.species_details, name="species_details"),
    url(r'^populations/$',main.population_overview, name="population_overview"),
    url(r'^populations/(?P<population_id>.*)/$',main.population_detail, name="population_detail"),
]

