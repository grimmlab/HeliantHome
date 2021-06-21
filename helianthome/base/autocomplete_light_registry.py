"""
Autocomplete Light Registry for global search
"""
from dal import autocomplete

from main.models import Phenotype, Study, Individual, Accession, Population


class GlobalSearchAutocomplete(autocomplete.Select2QuerySetView):
    """
    Global search autocomplete configuration class
    """
    def get_queryset(self):
        qs = Phenotype.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        
        return qs
    
    '''
    choices = (Phenotype.objects.all(),
               Study.objects.all(),
               Accession.objects.all(),
               Individual.objects.all(),
               Population.objects.all(),
              )
    search_fields = (('name', 'category','sub_category'), #phenotype search field
                     ('name',), #study search field
                     ('accession_id',), 
                     ('individual_id',), 
                     ('population_id','country','sitename'), 
                     ) 

    attrs = {'placeholder':'Search a phenotype, study, population id, country, sitename (e.g. DTF)',
             'data-autocomplete-minimum-characters':1}

    widget_attrs = {'class':'form-control'}

    #Individual Choice Render Format
    choice_html_format = u"<span class='block' data-value='%s'>%s</span>"

    #Render Choide
    def choice_html(self, choice):
        return self.choice_html_format % (self.choice_value(choice), self.choice_label(choice))

    #Render Autocomplete HTML for different search results
    def autocomplete_html(self):
        html = ""
        print("ASDAD")
        for choice in self.choices_for_request():
            if isinstance(choice, Phenotype):
                html += ("<a href='phenotype/%d'>%s</a>" % (choice.id, self.choice_html(choice)))
            elif isinstance(choice, Study):
                html += ("<a href='study/%d'>%s</a>" % (choice.id, self.choice_html(choice)))
            elif isinstance(choice, Accession):
                html += ("<a href='accession/%d'>%s</a>" % (choice.id, self.choice_html(choice)))
            elif isinstance(choice, Individual):
                html += ("<a href='individual/%d'>%s</a>" % (choice.id, self.choice_html(choice)))
            elif isinstance(choice, Population):
                html += ("<a href='population/%d'>%s</a>" % (choice.id, self.choice_html(choice)))
        return html

    autocomplete_light.register(GlobalSearchAutocomplete)
    '''
