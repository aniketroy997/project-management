from django.shortcuts import render
from django.contrib.auth.models import User

from api.models import *
from api.serializer import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
#-----------------------User Model---------------------------------

@api_view(['GET'])
def userList(request):
    user = User.objects.filter(is_superuser=False).order_by('first_name')
    serializer = UserSerializer(user, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def userDetailList(request):
    user = UserProfileDetail.objects.filter().order_by('name')
    serializer = UserProfileDetailSerializer(user, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def userGroup(request, pk):
    userGroup = UserGroup.objects.filter(project_Id = pk)
    serializer = UserGroupSerializer(userGroup, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def createUserGroup(request):
    serializer = UserGroupSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def userGroupDelete(request, pk, uk):
    userGroup = UserGroup.objects.get(project_Id = pk, user = uk)
    userGroup.delete()

    return Response('Item Deleted Successsfully')


@api_view(['GET'])
def managerGroup(request, pk):
    managerGroup = ManagerGroup.objects.filter(project_Id = pk)
    serializer = ManagerGroupSerializer(managerGroup, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def createManagerGroup(request):
    serializer = ManagerGroupSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def managerGroupDelete(request, pk, uk):
    managerGroup = ManagerGroup.objects.get(project_Id = pk, user = uk)
    managerGroup.delete()

    return Response('Item Deleted Successsfully')

@api_view(['GET'])
def projectUserList(request, pk, wpk):
    wp = WorkPackage.objects.get(id = wpk)
    final_list = User.objects.filter(usergroup__project_Id = pk, userprofiledetail__department = wp.department_id)

    serializer = UserSerializer(final_list, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def UsersProjectList(request, uk):
    projectList = UserGroup.objects.filter(user = uk)

    final_list=[]

    for project in projectList:
        
        element = Project.objects.get(id = project.project_Id_id)
        final_list.append(element)

    serializer = ProjectSerializer(final_list, many = True)
    return Response(serializer.data)