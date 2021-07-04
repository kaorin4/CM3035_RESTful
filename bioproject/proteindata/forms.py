from django import forms
from django.forms import ModelForm
from .models import *
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class ProteinForm(forms.Form):

    protein_id = forms.CharField()
    # length = forms.IntegerField(validators=[MinValueValidator(1)])


class ProteinDomainForm(ModelForm):

    start = forms.IntegerField(validators=[MinValueValidator(1)])
    stop = forms.IntegerField(validators=[MinValueValidator(1)])

    def clean(self):
        cleaned = super(ProteinDomainForm, self).clean()
        start =  cleaned.get('start')
        stop =  cleaned.get('stop')

        if stop < start:
            raise forms.ValidationError(u'Stop should be larger than start')

    class Meta:
        model = Protein
        fields = ['start', 'stop']
    

