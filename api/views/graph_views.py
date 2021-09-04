from django.shortcuts import render

from api.models import *
from api.serializer import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from django.db.models import Count
from django.db.models import Q
#--------------------Graphs Data Views-------------------

def SubworkpackageByResponsible(request, pid):
    
    user_List = User.objects.annotate(package_count=Count('subworkpackage__responsible', 
    filter=Q(subworkpackage__project_Id = pid)
    )).filter(is_superuser = False, usergroup__project_Id = pid)

    data = list(user_List.values('first_name', 'last_name','package_count'))
    
    return JsonResponse(data, safe=False)

def SubworkpackageByStatus(request, pid):
    
    status_List = State.objects.annotate(package_count=Count('subworkpackage__state', filter=Q(subworkpackage__project_Id = pid)))
    
    data = list(status_List.values())
    
    return JsonResponse(data, safe=False)

def startPlannedDate(request, pid):
    
    query_result = (SubWorkPackage.objects
    .exclude(date_of_start=None).order_by('date_of_start').filter(project_Id = pid)
    )

    start_data = list(query_result.values('date_of_start'))
    
    return JsonResponse(start_data, safe=False)

def endPlannedDate(request, pid):
    
    query_result = (SubWorkPackage.objects
    .exclude(date_of_end=None).order_by('date_of_end').filter(project_Id = pid)
    )
    
    end_data = list(query_result.values('date_of_end'))

    return JsonResponse(end_data, safe=False)

def projectStartDate(request, pid):
    query_result = Project.objects.filter(id = pid)

    data = list(query_result.values('date_of_creation'))
    
    return JsonResponse(data, safe=False)

def startActualDate(request, pid):
    query_result = (SubWorkPackage.objects
    .exclude(actual_date_of_start=None).order_by('actual_date_of_start').filter(project_Id = pid)
    )

    start_data = list(query_result.values('actual_date_of_start'))
    
    return JsonResponse(start_data, safe=False)
    

def endActualDate(request, pid):
    query_result = (SubWorkPackage.objects
    .exclude(actual_date_of_end=None).order_by('actual_date_of_end').filter(project_Id = pid)
    )
    
    end_data = list(query_result.values('actual_date_of_end'))
    
    return JsonResponse(end_data, safe=False)

def StateByWeek(request, pid):
    
    state_List = SubWorkPackage.objects.filter(project_Id = pid)
    
    data = list(state_List.values('date_of_state1', 'date_of_state2', 'date_of_state3', 'date_of_state4'))
    
    return JsonResponse(data, safe=False)