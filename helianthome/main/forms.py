from django import forms

from main import models

class PopulationFilter(forms.Form):
    species = forms.ModelChoiceField(queryset=models.Population.objects.order_by('species__species').values_list('species__species', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select","aria-label":"Select a Taxa"}),required=False)
    country = forms.ModelChoiceField(queryset=models.Population.objects.order_by('country').values_list('country', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select"}),required=False)
    sitename = forms.ModelChoiceField(queryset=models.Population.objects.order_by('sitename').values_list('sitename', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select"}),required=False)
    cultivated = forms.ModelChoiceField(queryset=models.Population.objects.order_by('species__cultivated').values_list('species__cultivated', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select"}),required=False)
    #class Meta:
    #    model = models.Population
    #    fields = ['species']

class PhenotypeFilter(forms.Form):
    species = forms.ModelChoiceField(queryset=models.Phenotype.objects.order_by('species__species').values_list('species__species', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select","aria-label":"Select a Taxa"}),required=False)
    cultivated = forms.ModelChoiceField(queryset=models.Phenotype.objects.order_by('species__cultivated').values_list('species__cultivated', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select"}),required=False)
    category = forms.ModelChoiceField(queryset=models.Phenotype.objects.order_by('category').values_list('category', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select"}),required=False)
    subcategory = forms.ModelChoiceField(queryset=models.Phenotype.objects.order_by('sub_category').values_list('sub_category', flat=True).distinct(),widget=forms.Select(attrs={"class":"form-select"}),required=False)
    #class Meta:
    #    model = models.Population
    #    fields = ['species']
