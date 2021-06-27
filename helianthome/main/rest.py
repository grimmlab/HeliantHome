from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count
from django.http import FileResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.views import APIView

from rest_framework_csv.renderers import CSVRenderer

from main.serializers import PhenotypeListSerializer, PhenotypeValueSerializer
from main.serializers import SpeciesListSerializer, PopulationListSerializer
from main.serializers import IndividualListSerializer, AccessionListSerializer
from main.renderer import PhenotypeListRenderer, PhenotypeValueRenderer, PLINKRenderer
from main.renderer import SpeciesListRenderer, PopulationListRenderer
from main.renderer import IndividualListRenderer, AccessionListRenderer
from main.models import Phenotype, Species, Population
from main.models import Individual, Accession

import re,os,array
import tempfile
import shutil

'''
List all phenotypes
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((PhenotypeListRenderer,JSONRenderer))
def phenotype_list(request,format=None):
    """
    List all available phenotypes
    ---
    serializer: PhenotypeListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    phenotypes = Phenotype.objects.annotate(num_values=Count('phenotypevalue'))
    if request.method == "GET":
        serializer = PhenotypeListSerializer(phenotypes,many=True)
        return Response(serializer.data)

'''
Detail information about phenotype
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((PhenotypeListRenderer,JSONRenderer))
def phenotype_detail(request,q,format=None):
    """
    Detailed information about the phenotype
    ---
    parameters:
        - name: q
          description: the id of the phenotype
          required: true
          type: string
          paramType: path
    serializer: PhenotypeListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    try:
        phenotype = Phenotype.objects.annotate(num_values=Count('phenotypevalue')).get(pk=int(q))
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = PhenotypeListSerializer(phenotype,many=False)
        return Response(serializer.data)

'''
Get all phenotype values
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((PhenotypeValueRenderer,JSONRenderer,PLINKRenderer))
def phenotype_value(request,q,format=None):
    """
    List of the phenotype values
    ---
    parameters:
        - name: q
          description: the id of the phenotype
          required: true
          type: string
          paramType: path
    serializer: PhenotypeValueSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    try:
        phenotype = Phenotype.objects.get(pk=int(q))
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        pheno_infos = phenotype.phenotypevalue_set.prefetch_related('phenotype_link__individual')
        value_serializer = PhenotypeValueSerializer(pheno_infos,many=True)
        return Response(value_serializer.data)

'''
List all species
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((SpeciesListRenderer,JSONRenderer))
def species_list(request,format=None):
    """
    List all available species
    ---
    serializer: SpeciesListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    species = Species.objects.all()
    if request.method == "GET":
        serializer = SpeciesListSerializer(species,many=True)
        return Response(serializer.data)

'''
Detail information about species
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((SpeciesListRenderer,JSONRenderer))
def species_detail(request,q,format=None):
    """
    Detailed information about the species
    ---
    parameters:
        - name: q
          description: the id of the species
          required: true
          type: string
          paramType: path
    serializer: PhenotypeListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    try:
        species = Species.objects.get(ncbi_id=q)
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = SpeciesListSerializer(species,many=False)
        return Response(serializer.data)

'''
List all populations
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((CSVRenderer,JSONRenderer))
def population_list(request,format=None):
    """
    List all available populations
    ---
    serializer: PopulationListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    population = Population.objects.all()
    if request.method == "GET":
        serializer = PopulationListSerializer(population,many=True)
        return Response(serializer.data)

'''
Detail information about population
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((CSVRenderer,JSONRenderer))
def population_detail(request,q,format=None):
    """
    Detailed information about the population
    ---
    parameters:
        - name: q
          description: the id of the population
          required: true
          type: string
          paramType: path
    serializer: PhenotypeListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    try:
        population = Population.objects.get(population_id=q)
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = PopulationListSerializer(population,many=False)
        return Response(serializer.data)

'''
List all individuals
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((IndividualListRenderer,JSONRenderer))
def individual_list(request,format=None):
    """
    List all available individuals
    ---
    serializer: PopulationListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    individual = Individual.objects.all()
    if request.method == "GET":
        serializer = IndividualListSerializer(individual,many=True)
        return Response(serializer.data)

'''
Detail information about individual
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((IndividualListRenderer,JSONRenderer))
def individual_detail(request,q,format=None):
    """
    Detailed information about the individual
    ---
    parameters:
        - name: q
          description: the id of the individual
          required: true
          type: string
          paramType: path
    serializer: PhenotypeListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    try:
        individual = Individual.objects.get(individual_id=q)
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = IndividualListSerializer(individual,many=False)
        return Response(serializer.data)

'''
List all accessions
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((AccessionListRenderer,JSONRenderer))
def accession_list(request,format=None):
    """
    List all available accessions
    ---
    serializer: PopulationListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    accession = Accession.objects.all()
    if request.method == "GET":
        serializer = AccessionListSerializer(accession,many=True)
        return Response(serializer.data)

'''
Detail information about accession
'''
@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@renderer_classes((AccessionListRenderer,JSONRenderer))
def accession_detail(request,q,format=None):
    """
    Detailed information about the accession
    ---
    parameters:
        - name: q
          description: the id of the accession
          required: true
          type: string
          paramType: path
    serializer: PhenotypeListSerializer
    omit_serializer: false
    produces:
        - text/csv
        - application/json
    """
    try:
        accession = Accession.objects.get(accession_id=q)
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = AccessionListSerializer(accession,many=False)
        return Response(serializer.data)
