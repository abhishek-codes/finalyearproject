from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import get_template

def home_page(request):
    template_name = "home.html"
    # template_obj = get_template(template_name)
    return redirect('/forum')
 