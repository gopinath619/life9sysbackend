from django.shortcuts import render

# Create your views here.

import random
import string

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import hashlib
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import userProfile, Token, CourseNames, Chapters, Topics


def encrypt_password(password):
    encrypt = hashlib.md5(password.encode('utf-8')).hexdigest()
    print ("ghgjgjghjgjgjgjgj",encrypt)
    return encrypt

def authentication(tokennumber):
    try:
        token_object = Token.objects.get(token=tokennumber)
        return token_object.user
    except Exception as e:
        # print e
        return Response("Session Expired", status=status.HTTP_401_UNAUTHORIZED)

def random_number():
    chars = string.ascii_uppercase + string.digits
    randomnum = ''.join(random.choice(chars) for _ in range(50))
    check = Token.objects.filter(token=randomnum)
    if check:
        random_number()
    return randomnum


def token(tokennumber, profile):
    token_object = Token()
    token_object.token = tokennumber
    token_object.role = profile.role
    token_object.user = profile.id
    token_object.save()

@api_view(['POST'])
def teachersignup(request):
    print('request-----------------------------------',request.data)
    full_name = request.data['firstName']
    mobile_number = request.data['mobile']
    password = request.data['password']
    role=request.data['role']
    try:
        user = User.objects.get(username=mobile_number)
        if user:
            return Response("User already exists", status=status.HTTP_200_OK)
    except User.DoesNotExist:
        try:
            print("i m inside")
            with transaction.atomic():
                print("hiiiiiiiiiiiiiii")
                user1=User()
                user1.username = mobile_number
                user1.password = encrypt_password(password)
                user1.last_name = ""
                user1.first_name = full_name
                user1.is_active = True
                user1.save()
                userid = User.objects.get(id=user1.id)
                print("mobile", userid)
                profile = userProfile()
                profile.user = userid
                profile.full_name = full_name
                profile.mobile_number = mobile_number
                profile.role=role
                profile.save()
            return Response("Registration success", status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Registration failed", status=status.HTTP_200_OK)



@api_view(['POST'])
def login_user(request):
    print("login---------",request.data)
    mobile = request.data['mobile']
    password = encrypt_password(request.data['password'])
    user = User.objects.filter(username = mobile,password = password, is_active = True)
    if user:
        profile = userProfile.objects.filter(mobile_number = mobile)
        token_number = random_number()
        token(token_number, profile[0])
        data = {'role': profile[0].role, 'token': token_number}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {'role': 'mobile number or password wrong', 'token': 'error'}
        return Response(data)

@api_view(['POST'])
def logout(request):
    token_number = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    token_number.delete()
    return Response('loggedout', status=status.HTTP_200_OK)

# @csrf_exempt
# @api_view(['POST'])
# def login_user(request):
#     print('--------------',request.data)
#     user_details = authenticate(username=request.data['mobile'],password=request.data['password'])
#     print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii---------------------',user_details)
#     if user_details:
#         print('------------------')
#         # profile = userProfile.objects.filter(mobile_number=request.data['mobile'])
#         login(request,user_details)
#         return Response(request)
#     else:
#         return Response('login fail')
#
# @api_view(['POST'])
# def logout_user(request):
#     logout(request)
#     return render('logout')


@api_view(['POST'])
def addnewcourse(request):
    user_id = authentication(request.META['HTTP_AUTHORIZATION'])
    try:
       obj=CourseNames()
       obj.name = request.data['name']
       obj.teacher_id = user_id
       obj.save()
       return Response("add course success", status=status.HTTP_200_OK)
    except Exception as e:
        print ("Exception raised",e)
        return Response("add course failed", status=status.HTTP_200_OK)


@api_view(['GET'])
def getallcourses(request):
    user_id = authentication(request.META['HTTP_AUTHORIZATION'])
    try:
      mycourses = CourseNames.objects.filter(teacher_id=user_id).values()
      print("my courses",mycourses)
      return Response(mycourses, status=status.HTTP_200_OK)
    except Exception as e:
        print ("Exception raised",e)
        return Response("Error", status=status.HTTP_200_OK)


@api_view(['POST'])
def addnewchapter(request):
    print("data is",request.data)
    user_id = authentication(request.META['HTTP_AUTHORIZATION'])

    try:
        obj=Chapters()
        obj.chaptername = request.data['chapter']
        obj.course_id = request.data['course']
        obj.save()
        return Response("add chapter success", status=status.HTTP_200_OK)
    except Exception as e:
        print ("Exception raised",e)
        return Response("add chapter failed", status=status.HTTP_200_OK)



@api_view(['GET'])
def getchapters(request):
      user_id = authentication(request.META['HTTP_AUTHORIZATION'])
      mychapters = Chapters.objects.filter(teacher_id=user_id).values()
      print("my courses are", mychapters)
      for i in mychapters:
          mycourses = CourseNames.objects.filter(teacher_id=user_id).values()
          i['name']=mycourses[0]['name']
      print("my chapters are---0000000000000000000000000000000000000000000000000000000----------------- ",mychapters)
      return Response(mychapters, status=status.HTTP_200_OK)


@api_view(['POST'])
def addnewtopic(request):
    print("data is",request.data)
    user_id = authentication(request.META['HTTP_AUTHORIZATION'])

    try:
        obj=Topics()
        obj.chapter_id = request.data['chapter']
        obj.teacher_id = user_id
        obj.topicName = request.data['topic']
        obj.save()
        return Response("add topic success", status=status.HTTP_200_OK)
    except Exception as e:
        print ("Exception raised",e)
        return Response("add topic failed", status=status.HTTP_200_OK)

@api_view(['GET'])
def gettopics(request):
      print("dasdsadsadsadsadad",request.data)
      user_id = authentication(request.META['HTTP_AUTHORIZATION'])
      print("dasdsadsadsadsadad",user_id)

      mytopic = Topics.objects.filter(teacher_id=user_id).values()
      print("my courses are", mytopic)
      # for i in mytopic:
      #     print("i value is",i)
      #     mytopics = Chapters.objects.filter(teacher_id=user_id).values()
      #     i['topicName']=mytopics[0]['topicName']
      # print("my chapters are---0000000000000000000000000000000000000000000000000000000----------------- ",mytopic)
      return Response(mytopic, status=status.HTTP_200_OK)