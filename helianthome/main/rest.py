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

from main.serializers import PhenotypeListSerializer, PhenotypeValueSerializer
from main.renderer import PhenotypeListRenderer, PhenotypeValueRenderer, PLINKRenderer
from main.models import Phenotype

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
