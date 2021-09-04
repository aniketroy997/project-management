from django.shortcuts import render
from django.contrib.auth.models import User
from api.models import *
from django.views.generic import View
from api.serializer import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from api.filters import *

from datetime import datetime
#----------------------Sub Work Packages Views --------------------------------

@api_view(['GET'])
def subWorkPackageList(request):
    subSubWorkPackage = SubWorkPackage.objects.all()
    serializer = SubWorkPackageSerializer(subSubWorkPackage, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def subWorkPackageCreate(request):
    serializer = SubWorkPackageSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
    
@api_view(['GET'])
def subWorkPackageDetail(request, pk):
    subSubWorkPackage = SubWorkPackage.objects.get(id = pk)
    serializer = SubWorkPackageSerializer(subSubWorkPackage, many = False)

    return Response(serializer.data)

'''@api_view(['POST'])
def subWorkPackageUpdate(request, pk):
    subSubWorkPackage = SubWorkPackage.objects.get(id = pk)
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
'''
@api_view(['DELETE'])
def subWorkPackageDelete(request, pk):
    subSubWorkPackage = SubWorkPackage.objects.get(id = pk)
    subSubWorkPackage.delete()

    return Response('Item Deleted Successsfully')


@api_view(['GET'])
def allSubWorkPackage(request, wpk):
    subSubWorkPackage = SubWorkPackage.objects.filter(workPackage = wpk)
    serializer = SubWorkPackageSerializer(subSubWorkPackage, many = True)

    return Response(serializer.data)

class updatePackageUser(View):
    def post(self, request):
        data = request.POST
        userId = data.get('responsible')
        SWPid = data.get('subworkpackage')
        subWorkPackage = SubWorkPackage.objects.get(id = SWPid)
        if(userId != "null"):
            user = User.objects.get(id = userId)
            subWorkPackage.responsible = user
        else:
            subWorkPackage.responsible = None

        subWorkPackage.save()
        return JsonResponse({'Response':'Successfully Saved'}, status=200)

#------------------Update status Sub Work Package from id---------------------

@api_view(['POST'])
def updateSubPackageState(request):
    data = request.POST
    SWPid = data.get('id')
    subWorkPackage = SubWorkPackage.objects.get(id = SWPid)
    stateId = data.get('state')
    state = State.objects.get(id = stateId)
    subWorkPackage.state = state
    
    if(data.get('state') == '2'):
        subWorkPackage.date_of_state2 = data.get('actual_date')
    elif(data.get('state') == '3'):
        subWorkPackage.date_of_state3 = data.get('actual_date')
        subWorkPackage.actual_date_of_start = data.get('actual_date')
    elif(data.get('state') == '4'):
        subWorkPackage.date_of_state4 = data.get('actual_date')
        subWorkPackage.actual_date_of_end = data.get('actual_date')
    elif(data.get('state') == '2'):
        subWorkPackage.actual_date_of_start = None
        
    subWorkPackage.save()
    
    return JsonResponse({'Response':'Successfully Saved'}, status=200)


#------------------Sub Work Package from work package key---------------------


#-------------------User SubworkPackages----------------------------------
'''
@api_view(['GET'])
def allUserSubWorkPackage(request, uk):
    subSubWorkPackage = SubWorkPackage.objects.filter(responsible = uk)
    filter_data = CardFilter(request.GET, queryset=subSubWorkPackage)
    subSubWorkPackage = filter_data.qs
    serializer = SubWorkPackageSerializer(subSubWorkPackage, many = True)

    return Response(serializer.data)
'''
@api_view(['GET'])
def singleUserSubWorkPackage(request, uk, pk):
    subSubWorkPackage = SubWorkPackage.objects.filter(responsible = uk, project_Id = pk)
    print(subSubWorkPackage)
    filter_data = CardFilter(request.GET, queryset=subSubWorkPackage)
    subSubWorkPackage = filter_data.qs
    serializer = SubWorkPackageSerializer(subSubWorkPackage, many = True)

    return Response(serializer.data)