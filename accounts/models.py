from django.db import models
from contact.models import Contato
from django import forms

class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = []
