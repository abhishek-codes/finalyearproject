from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

def home_page(request):
    template_name = "home.html"
    # template_obj = get_template(template_name)
    return render(request,template_name)
 