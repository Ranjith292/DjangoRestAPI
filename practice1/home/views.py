from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from django.http import Http404
from .serialializer import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.

@api_view(['POST'])
def login(request):
    user=get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"Not found"})
    token, created=Token.objects.get_or_create(user=user)
    serializer=UserSerializer(instance=user)
    return Response({"token":token.key,"user":serializer.data})

@api_view(['POST'])
def signup(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token=Token.objects.create(user=user)
        return Response({"token":token.key,"user":serializer.data})
    return Response({serializer.errors})

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.username))

class StudentView(APIView):
    def get(self,request):
        student_obj=Student.objects.all()
        serializer=StudentSerializer(student_obj,many=True)
        return Response({
            "status":200,
            "data":serializer.data
        })
    
    def post(self,request):
        data=request.data
        serializer=StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            "status":200,
            "data":serializer.data
            })
        return Response({
            "status":400,
            "data":serializer.errors
        })
    
    def patch(self,request):
        data=request.data
        if not data.get('uid'):
            return Response({
                "message":"Uid is mandatory"
            })
        obj=Student.objects.get(uid=data.get('uid'))
        serializer=StudentSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":200,
                "data":serializer.data
            })
        return Response({
            "status":400,
            "data":serializer.errors
        })
    
    def put(self,request):
        data=request.data
        if not data.get('uid'):
            return Response({
                "message":"Uid is mandatory"
            })
        obj=Student.objects.get(uid=data.get('uid'))
        serializer=StudentSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":200,
                "data":serializer.data
            })
        return Response({
            "status":400,
            "data":serializer.errors
        })
    
    def delete(self,request,uid):
        student=Student.objects.get(uid=uid)
        student.delete()
        return Response({
            "status":200,
            "data":"Record deleted"
        })