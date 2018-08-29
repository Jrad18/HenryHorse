from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
import json

from .models import Forms

# Create your views here.

def index(request):
    template = loader.get_template('Forms/index.html')
    context = {
        'Forms': Forms,
        'formData': Forms.objects.get(id=1).datadump(),
    }
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template('Forms/add.html')
    context = {
        'Form': Forms.objects.get(id=1),
        'formData': Forms.objects.get(id=1).datadump(),

    }
    return HttpResponse(template.render(context, request))

def newForm(request, form_id):
    thisForm = get_object_or_404(Forms, pk=form_id)
    thisForm.form_data = json.loads(request.POST['formData'])
    thisForm.save()
    return HttpResponseRedirect(reverse('Form'))