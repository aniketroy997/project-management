from django.shortcuts import render

from projects.forms import *
from api.models import *
from api.serializer import *

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.forms.models import model_to_dict
from django.http import JsonResponse

#--------------------------Work Packages Views-------------------------
@api_view(['GET'])
def workPackageList(request):
    workPackage = WorkPackage.objects.all()
    serializer = WorkPackageSerializer(workPackage, many = True)
    return Response(serializer.data)

from collections import defaultdict

@api_view(['GET'])
def workPackagesByDepartment(request, uk, dep_id):
    temp = list( ManagerGroup.objects.values_list('project_Id', flat=True).filter(user = uk) )
    workPackage = WorkPackage.objects.filter(project_Id__in = temp, department = dep_id)

    for wp in range(0, len(workPackage)):
        subWorkPackages = SubWorkPackage.objects.filter(workPackage = workPackage[wp])
        d = defaultdict(int)
        for swp in subWorkPackages:
            d[swp.state_id] += 1
        
        max_key = max(d, key=d.get)
        
        workPackage[wp].state = max_key

    serializer = WorkPackageSerializer(workPackage, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def projectWorkPackagesByDepartment(request, uk, dep_id, pk):
    temp = list( ManagerGroup.objects.values_list('project_Id', flat=True).filter(user = uk) )
    workPackage = WorkPackage.objects.filter(project_Id__in = temp, department = dep_id, project_Id = pk)

    for wp in range(0, len(workPackage)):
        subWorkPackages = SubWorkPackage.objects.filter(workPackage = workPackage[wp])
        d = defaultdict(int)
        for swp in subWorkPackages:
            d[swp.state_id] += 1
        
        max_key = max(d, key=d.get)
        
        workPackage[wp].state = max_key

    serializer = WorkPackageSerializer(workPackage, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def workPackagesList(request, pk, dep_id):
    workPackage = WorkPackage.objects.filter(project_Id = pk, department = dep_id)
    serializer = WorkPackageSerializer(workPackage, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def workPackageCreate(request):
    serializer = WorkPackageSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
    
@api_view(['GET'])
def workPackageDetail(request, pk):
    workPackage = WorkPackage.objects.get(id = pk)
    serializer = WorkPackageSerializer(workPackage, many = False)

    return Response(serializer.data)

@api_view(['POST'])
def workPackageUpdate(request, pk):
    workPackage = WorkPackage.objects.get(id = pk)
    serializer = WorkPackageSerializer(instance = workPackage, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def workManualPackageUpdate(request, pk):
    
    workPackage = WorkPackage.objects.get(id = pk)
    form = WorkPackageEditForm(request.POST)

    workPackage.description = form.data.get('description')
    if(form.data.get('title') != ""):
        workPackage.title = form.data.get('title')
    if(form.data.get('date_of_end') != ""):
        workPackage.date_of_end = form.data.get('date_of_end')
        temp = datetime.strptime((form.data.get('date_of_end')), '%Y-%m-%d')
        
    if(form.data.get('date_of_start') != ""):
        workPackage.date_of_start = form.data.get('date_of_start')
    if(form.data.get('date_of_end') != "" and form.data.get('date_of_start') != ""):
        duration = datetime.strptime((form.data.get('date_of_end')), '%Y-%m-%d') - datetime.strptime((form.data.get('date_of_start')), '%Y-%m-%d')
        workPackage.duration = duration.days
    if(form.data.get('priority') != ""):
        workPackage.priority = form.data.get('priority')
    if(form.data.get('efforts_planned') != ""):
        workPackage.efforts_planned = form.data.get('efforts_planned')

    workPackage.save()

    return JsonResponse({'WorkPackage':model_to_dict(workPackage)}, status=200)


@api_view(['DELETE'])
def workPackageDelete(request, pk):
    workPackage = WorkPackage.objects.get(id = pk)
    workPackage.delete()

    return Response('Item Deleted Successsfully')