from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class HtmlSectionView(TemplateView):
    template_name = 'html_section/index.html'
