from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Asset, AssetProvider

class AssetRequestForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_type', 'prompt', 'style', 'user', 'provider']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))
