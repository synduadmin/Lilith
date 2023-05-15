# leads app, forms.py
from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    ip_address = forms.GenericIPAddressField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Lead
        fields = ['interested_as', 
                  'name', 
                  'email', 
                  #'message', 
                  'ip_address']
