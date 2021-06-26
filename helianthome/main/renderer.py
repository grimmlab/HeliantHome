from rest_framework_csv.renderers import CSVRenderer
from rest_framework import renderers

'''
Renderer class for alternative ordering of the CSV output
'''
class PhenotypeListRenderer(CSVRenderer):
    header = ['species','phenotype_id','phenotype_name','num_values','description',
              'method','category','subcategory','type','easygwas_link',
              'ontology_name','ontology_id']

class PhenotypeValueRenderer(CSVRenderer):
    header = ['species','phenotype_id','phenotype_name','population','id','phenotype_value']

'''
Custom File Renderer
'''
class PLINKRenderer(renderers.BaseRenderer):
    media_type = "application/plink"
    format = "plink"

    def render(self,data,media_type=None,renderer_context=None):
        if data is None:
            return "No Data Found"
        plink = "FID IID \"" + data[0]['phenotype_name'].replace(' ','_') + "\"\n"
        for element in data:
            if not ("id" in element):
                return "Wrong Data Format"
            plink += str(element['id']) + " " + str(element['id']) + " " + str(element['phenotype_value']) + "\n"
        return plink
