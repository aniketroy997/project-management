from django.shortcuts import render
from django.views.generic import View

from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *
from api.serializer import *

from projects.forms import *

from django.contrib.auth.decorators import login_required

from datetime import datetime

from django.apps import apps



#-----------------------Kanban Field--------------------------

@api_view(['GET'])
def stateList(request):
    state = State.objects.all()
    serializer = StateSerializer(state, many = True)
    
    return Response(serializer.data)

#----------------------------Increasing code reuse--------------------------------


@api_view(['POST'])
def subWorkPackageUpdate(request, pk):
    swpModelObject = apps.get_model(app_label='api', model_name='SubWorkPackage')
    subSubWorkPackage = swpModelObject.objects.get(id = pk)
    form = SubWorkPackageEditForm(request.POST)

    subSubWorkPackage.description = form.data.get('description')
    if(form.data.get('title') != "" and form.data.get('title') != None):
        subSubWorkPackage.title = form.data.get('title')
    if(form.data.get('date_of_end') != "" and form.data.get('date_of_end') != None):
        subSubWorkPackage.date_of_end = form.data.get('date_of_end')
        temp = datetime.strptime((form.data.get('date_of_end')), '%Y-%m-%d')
    if(form.data.get('date_of_start') != "" and form.data.get('date_of_start') != None):
        subSubWorkPackage.date_of_start = form.data.get('date_of_start')
    if(form.data.get('date_of_end') != "" and form.data.get('date_of_start') != "" and form.data.get('date_of_end') != None and form.data.get('date_of_start') != None):
        duration = datetime.strptime((form.data.get('date_of_end')), '%Y-%m-%d') - datetime.strptime((form.data.get('date_of_start')), '%Y-%m-%d')
        subSubWorkPackage.duration = duration.days    
    if(form.data.get('priority') != "" and form.data.get('priority') != None):
        subSubWorkPackage.priority = form.data.get('priority')
    if(form.data.get('efforts_planned') != ""):
        subSubWorkPackage.efforts_planned = form.data.get('efforts_planned')
    subSubWorkPackage.save()

    return JsonResponse({'subSubWorkPackage':model_to_dict(subSubWorkPackage)}, status=200)

@api_view(['GET'])
def allUserSubWorkPackage(request, uk):
    swpModelObject = apps.get_model(app_label='api', model_name='SubWorkPackage')
    subSubWorkPackage = swpModelObject.objects.filter(responsible = uk)
    #filter_data = CardFilter(request.GET, queryset=subSubWorkPackage)
    #subSubWorkPackage = filter_data.qs
    serializer = SubWorkPackageSerializer(subSubWorkPackage, many = True)

    return Response(serializer.data)