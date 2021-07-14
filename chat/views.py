# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from six import python_2_unicode_compatible
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.template.context_processors import csrf
from django.conf import settings
from chat.models import Log, QA,AuthUser,AdminFlag
import sys, os
import base64
import logging
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import uuid, tempfile
import json
from collections import OrderedDict
from django.shortcuts import  redirect,render
import chat.forms
from django.views.generic import ListView
from .forms import create,ItemForm
from django.views.decorators.clickjacking import xframe_options_exempt
from datetime import datetime
from django import forms
from django.forms import formsets
from django.forms import models
import django.http
import chat.models
import chat.forms
import time


import uuid
# from django.contrib.auth.models import User

# from django.contrib.auth import get_user_model
# User = get_user_model()
import re
from django.contrib.auth import authenticate, login as django_login
# coding: utf-8
#import django_filters
#from rest_framework import viewsets, filters

from .models import QA
#from .serializer import QASerializer
#from django_filters.rest_framework import DjangoFilterBackend
import hashlib


import logging
from datetime import datetime,timedelta
logging.getLogger().setLevel(logging.DEBUG)



from django.utils.six import six
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


def has_digit(text):
    if re.search("\d", text):
        return True
    return False

def has_alphabet(text):
    if re.search("[a-zA-Z]", text):
        return True
    return False

#画面にウィジェットを表示する
@xframe_options_exempt
def index(request):
    if 'user' in request.session:
        if request.method != 'POST':
            para=request.session['user']
            checkAdmin = AuthUser.objects.filter(username=para).first().adminFlag

            if (checkAdmin == True):
                userKey = QA.objects.filter(userId=para).first().userKey

            else:
                Admin = AdminFlag.objects.filter(userId=para).first().adminUser;
                userKey = QA.objects.filter(userId=Admin).first().userKey


            request.session['userKey']=userKey
            return render(request, 'Chat.html')

        print ('request.POST:' + request.POST['userId'])
        insert_data = Log(userId=request.POST['userId'],
                          Question=request.POST['Question'],
                          AnswerNo=request.POST['AnswerNo'],
                          Answer=request.POST['Answer'],
                          Withdrawal=request.POST['Withdrawal'],
                          ScreenId="Admin"
                          )
        insert_data.save()
        #print ('request.session[user]:' + request.session['user'])
        paraUser=request.session['user']
        print ('request.session[user]:' + request.session['user'])
        userKey=QA.objects.filter(userId=paraUser).first().userKey
        context = {}
        context['userKey'] = userKey
        context['user'] = request.session['user']
        return render(request, 'Chat.html',context)

    elif 'userKey' in request.session:
        if request.method != 'POST':
            para = request.session['userKey']
            context = {}
            context['userKey'] = para
            context['user'] = request.session['user']
            return render(request, 'Chat.html', context)

        para = request.session['userKey']
        userId = QA.objects.filter(userKey=para).first().userId
        context = {}
        insert_data = Log(userId=userId,
                          Question=request.POST['Question'],
                          AnswerNo=request.POST['AnswerNo'],
                          Answer=request.POST['Answer'],
                          Withdrawal=request.POST['Withdrawal']
                          )
        insert_data.save()
        userKey = QA.objects.get(userId=userId).userKey
        context = {}
        context['userKey'] = userKey
        context['user'] = request.session['user']
        return render(request, 'Chat.html', context)
    else:
        if request.method != 'POST':
            return render(request, 'Chat.html')
        para = request.POST['userKey']
        userId = QA.objects.filter(userKey=para).first().userId
        insert_data = Log(userId=userId,
                          Question=request.POST['Question'],
                          AnswerNo=request.POST['AnswerNo'],
                          Answer=request.POST['Answer'],
                          Withdrawal=request.POST['Withdrawal']
                          )
        insert_data.save()
        context = {}
        return render(request, 'Chat.html', context)

#login画面　
def login(request):
    if 'user' in request.session:
        print('login' )

    if request.method == 'POST':
        login_form = chat.forms.LoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
           # django_login(request,user)
            request.session['user'] =username
            return django.http.HttpResponseRedirect('/top')
        else:
            error="ユーザー名またはパスワードが異なります。"
            #login_form.add_error(None, "ユーザー名またはパスワードが異なります。")
            d={
                'login_form': login_form,
                'error':error
            }
            return render(request, 'Login.html', d)
        return render(request, 'Login.html', {'login_form': login_form})
    else:
        login_form = chat.forms.LoginForm()
    return render(request, 'Login.html', {'login_form': login_form})

#log画面　fourfusion提供バージョンはなし
def log(request):
    print('log'+request.session['user'])
    userPara=request.session['user']
    logs= Log.objects.all().filter(userId=userPara).order_by('-DateTime')


    for log in logs:

        log.DateTime=log.DateTime+timedelta(hours=9)
    return render(request, 'Log.html',{'Logs':logs})

#トップページ
def topPage(request):
    print('top' +request.session['user'])
    return render(request, 'TopPage.html')

#QA画面
from distutils.util import strtobool
def qa(request):
    print('qa'+request.session['user'])
    userPara=request.session['user']
    #check
    checkAdmin=AuthUser.objects.filter(username=userPara).first().adminFlag
    print(checkAdmin)

    if(checkAdmin==True):
        userPara=userPara;
    else:
        userPara = AdminFlag.objects.filter(userId=userPara).first().adminUser;
    print(userPara)
    if request.method != 'POST':

        formset = create(userPara)
        #print('qa1234' + str(request.user))
        return render(request, 'QA.html', {'formset': formset,})

    if 'all_public' in request.POST:
        print('make all public')
        for qa in QA.objects.filter(userId=userPara):
            qa.is_public = True
            qa.save()
        return redirect(to='/qa')
    
    if 'all_test' in request.POST:
        print('make all test')
        for qa in QA.objects.filter(userId=userPara):
            qa.is_public = False
            qa.save()
        return redirect(to='/qa')


    insertNum = int(request.POST['buttom'])   # formは０からはじまるため
    #print ('buttom:' + request.POST['buttom'])
    if request.POST['form-'+str(insertNum)+'-id']!='':
        serachNum=int(request.POST['form-'+str(insertNum)+'-id'])
        serachObj=QA.objects.filter(id=str(serachNum))

   # print ('serachObj:' + str(serachObj.values()))
    #print ('serachObj.count():'+str(serachObj.count()))

    if request.POST['form-'+str(insertNum)+'-id']=='':

        insert_data = QA(Keyword =request.POST['form-'+str(insertNum)+'-Keyword'],
                         Answer =request.POST['form-'+str(insertNum)+'-Answer'],
                         URL=request.POST['form-'+str(insertNum)+'-URL'],
                         userId=userPara,
                         is_public=bool(strtobool(request.POST['form-'+str(insertNum) + '-is_public'])),
                         Q1 =request.POST['form-'+str(insertNum)+'-Q1'],
                         Q2 =request.POST['form-'+str(insertNum)+'-Q2'],
                         Q3 =request.POST['form-'+str(insertNum)+'-Q3'],
                         Q4 =request.POST['form-'+str(insertNum)+'-Q4'],
                         Q5 =request.POST['form-'+str(insertNum)+'-Q5'],
                         A1 =request.POST['form-'+str(insertNum)+'-A1'],
                         A2 =request.POST['form-'+str(insertNum)+'-A2'],
                         A3 =request.POST['form-'+str(insertNum)+'-A3'],
                         A4 =request.POST['form-'+str(insertNum)+'-A4'],
                         A5  =request.POST['form-'+str(insertNum)+'-A5'],
                         IdPerUser=insertNum,
                         userKey=hashlib.md5(str(userPara)).hexdigest()
        )
        insert_data.save()
    else :
       # print ('hugahuga')
        print(request.POST['form-'+str(insertNum) + '-is_public'])
        print(bool(strtobool(request.POST['form-'+str(insertNum) + '-is_public'])))
        serachObj = QA.objects.get(id=str(serachNum))
        serachObj.Keyword = request.POST['form-'+str(insertNum)+'-Keyword']
        serachObj.Answer = request.POST['form-' + str(insertNum) + '-Answer']
        serachObj.URL = request.POST['form-' + str(insertNum) + '-URL']
        if bool(strtobool(request.POST['form-' + str(insertNum) + '-is_public'])):
            serachObj.is_public = True
        else:
            serachObj.is_public = False
        serachObj.Q1 = request.POST['form-' + str(insertNum) + '-Q1']
        serachObj.Q2 = request.POST['form-' + str(insertNum) + '-Q2']
        serachObj.Q3 = request.POST['form-' + str(insertNum) + '-Q3']
        serachObj.Q4 = request.POST['form-' + str(insertNum) + '-Q4']
        serachObj.Q5 = request.POST['form-' + str(insertNum) + '-Q5']
        serachObj.A1 = request.POST['form-' + str(insertNum) + '-A1']
        serachObj.A2 = request.POST['form-' + str(insertNum) + '-A2']
        serachObj.A3 = request.POST['form-' + str(insertNum) + '-A3']
        serachObj.A4 = request.POST['form-' + str(insertNum) + '-A4']
        serachObj.A5 = request.POST['form-' + str(insertNum) + '-A5']
        serachObj.save()

    num = 100 - QA.objects.filter(userId=userPara).count()
    formset = create(userPara)
    return redirect(to='/qa')
    # return HttpResponseRedirect(request,"/qa/#"+unicode(insertNum), {'formset': formset })
    #return render(request, 'QA.html', {'formset': formset ,'data':insertNum})

#setting画面
def setting(request):
    print('setting' + request.session['user'])

    Flag=True

    checkAdmin = AuthUser.objects.filter(username=request.session['user']).first().adminFlag
    #print(checkAdmin)

    if (checkAdmin == True):
        key = QA.objects.filter(userId=request.session['user']).first().userKey
    else:
        key = "権限がないため参照できません"

    return render(request, 'Setting.html',{'key': key})

def introduce(request):
    return render(request, 'Introduce.html')


def manual(request):
    return render(request, 'manual.html')

#作成中のユーザ管理画面
def userlist(request):
    userPara=request.session['user']
    if request.method == 'POST':
        form = chat.forms.SignUpForm(request.POST)
        if form.is_valid():
            form.author = userPara
            form.save()
            # login(request, user)
            return redirect(to='/userlist')
    form = chat.forms.SignUpForm()
    # users = User.objects.get(userId=userPara)
    return render(request,'Userlist.html', {'form': form})

#Test画面
def test(request):
    print('test'+request.session['user'])
    return render(request, 'Test.html')



#画面と紐つかないAPI
def api(request):

    if "userKey" in request.GET:
        # query_paramが指定されている場合の処理
        param_value = request.GET.get("userKey")
        print("param_value:"+param_value)
        qas=[]
        for qa in QA.objects.filter(userKey=param_value).order_by('IdPerUser'):
            reply = qa.Answer
            print '12345'+reply
            if qa.Q1 != '':
                reply = reply + '\n[option]' + '1.' + qa.Q1
            if qa.Q2 != '':
                reply = reply + '\n[option]' + '2.' + qa.Q2
            if qa.Q3 != '':
                reply = reply + '\n[option]' + '3.' + qa.Q3
            if qa.Q4 != '':
                reply = reply + '\n[option]' + '4.' + qa.Q4
            if qa.Q5 != '':
                reply = reply + '\n[option]' + '5.' + qa.Q5
            qa_dict = OrderedDict([
                ('IdPerUser', qa.IdPerUser),
                ('Keyword', qa.Keyword),
                ('Answer', reply),
                ('URL', qa.URL),
                ('userId', qa.userId),
                ('Q1', qa.Q1),
                ('Q2', qa.Q2),
                ('Q3', qa.Q3),
                ('Q4', qa.Q4),
                ('Q5', qa.Q5),
                ('A1', qa.A1),
                ('A2', qa.A2),
                ('A3', qa.A3),
                ('A4', qa.A4),
                ('A5', qa.A5),

            ])

            qas.append(qa_dict)

        data = qas
        json_str = json.dumps(data, ensure_ascii=False)

        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8',status=None)
        print(response)
        return response

    else:
       # print("else")
        data = {'error':'error1234'}
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)
        return response

#画面と紐つかないAPI
def apiFourfusion(request):
    start = time.time()

    if "key" in request.GET:
        if "message" in request.GET:
            if "sid" in request.GET:
                paramKey = request.GET.get("key")
                paramMessage = request.GET.get("message")
                paramSid = request.GET.get("sid")
                reply=""
                #paraIdPerUser=""
                i=0
                flg=0
                addOption = '[option]' + ' ' + paramMessage
                for log in Log.objects.all().filter(ScreenId=paramSid ):
                     if addOption in log.Answer:
                         flg=1
                         break
                if flg==1:
                   # print(str(log.Answer.encode('utf-8').strip()))
                    #print(log.AnswerNo)

                    #print(111111111111111111111)
                    beforeQa=QA.objects.filter(userKey=paramKey,IdPerUser=log.AnswerNo,is_public='1').first()
                   # print (str(beforeQa.Q1.encode('utf-8').strip()))
                    if beforeQa.Q1==paramMessage:
                            nextQa = QA.objects.filter(userKey=paramKey,IdPerUser=beforeQa.A1,is_public='1').first()
                            paraIdPerUser = nextQa.IdPerUser
                            reply = nextQa.Answer
                            if nextQa.Q1 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q1
                            if nextQa.Q2 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q2
                            if nextQa.Q3 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q3
                            if nextQa.Q4 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q4
                            if nextQa.Q5 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q5
                    elif beforeQa.Q2==paramMessage:
                            nextQa = QA.objects.filter(userKey=paramKey, IdPerUser=beforeQa.A2,is_public='1').first()
                            paraIdPerUser = nextQa.IdPerUser
                            reply = nextQa.Answer
                            if nextQa.Q1 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q1
                            if nextQa.Q2 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q2
                            if nextQa.Q3 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q3
                            if nextQa.Q4 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q4
                            if nextQa.Q5 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q5
                    elif beforeQa.Q3==paramMessage:
                            nextQa = QA.objects.filter(userKey=paramKey, IdPerUser=beforeQa.A3,is_public='1').first()
                            paraIdPerUser = nextQa.IdPerUser
                            reply = nextQa.Answer
                            if nextQa.Q1 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q1
                            if nextQa.Q2 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q2
                            if nextQa.Q3 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q3
                            if nextQa.Q4 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q4
                            if nextQa.Q5 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q5
                    elif beforeQa.Q4==paramMessage:
                            nextQa = QA.objects.filter(userKey=paramKey, IdPerUser=beforeQa.A4,is_public='1').first()
                            paraIdPerUser = nextQa.IdPerUser
                            reply = nextQa.Answer
                            if nextQa.Q1 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q1
                            if nextQa.Q2 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q2
                            if nextQa.Q3 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q3
                            if nextQa.Q4 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q4
                            if nextQa.Q5 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q5
                    elif beforeQa.Q5==paramMessage:
                            nextQa = QA.objects.filter(userKey=paramKey, IdPerUser=beforeQa.A5,is_public='1').first()
                            paraIdPerUser = nextQa.IdPerUser
                            reply = nextQa.Answer
                            if nextQa.Q1 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q1
                            if nextQa.Q2 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q2
                            if nextQa.Q3 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q3
                            if nextQa.Q4 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q4
                            if nextQa.Q5 != '':
                                reply = reply + '\n[option]' + ' ' + nextQa.Q5
                    else:
                            reply = QA.objects.filter(userKey=paramKey,is_public='1').order_by('IdPerUser').first().Answer
                else:
                    #print(22222222222222222222222)
                    for qa in QA.objects.filter(userKey=paramKey,is_public='1').order_by('IdPerUser'):
                        if(qa.Keyword!=''):
                            if qa.Keyword in paramMessage:
                                reply = qa.Answer
                                paraIdPerUser =qa.IdPerUser
                                if qa.Q1!='':
                                    reply=reply+'\n[option]'+' '+qa.Q1
                                if qa.Q2!='':
                                    reply=reply+'\n[option]'+' '+qa.Q2
                                if qa.Q3!='':
                                    reply=reply+'\n[option]'+' '+qa.Q3
                                if qa.Q4!='':
                                    reply=reply+'\n[option]'+' '+qa.Q4
                                if qa.Q5!='':
                                    reply=reply+'\n[option]'+' '+qa.Q5
                                break
                    if reply =="":
                        reply=QA.objects.filter(userKey=paramKey,is_public='1').order_by('IdPerUser').first().Answer
                        paraIdPerUser=QA.objects.filter(userKey=paramKey,is_public='1').order_by('IdPerUser').first().IdPerUser


                data = reply
                #json_str = data
                json_str=data.encode('utf-8').strip()
                response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)
                QA.objects.filter(userKey=paramKey,is_public='1').order_by('IdPerUser').first().userId
                insert_data = Log(userId=QA.objects.filter(userKey=paramKey).order_by('IdPerUser').first().userId,
                                      Question=paramMessage,
                                      AnswerNo=paraIdPerUser,
                                      Answer=reply,
                                      ScreenId=paramSid
                                      )
                insert_data.save()
                #print(reply)
                process_time = time.time() - start

                print(process_time)
                return response
            else:
                data = {'error': 'error3'}
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)
                # print(1234)
                return response

        else:
            data = {'error': 'error1'}
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)
            #print(1234)
            return response
        # query_paramが指定されている場合の処理
    else:
       # print("else")
        data = {'error':'error2'}
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)
        #print(4567)
        return response



#class QAViewSet(viewsets.ModelViewSet):
    #   queryset = QA.objects.order_by('IdPerUser')
    #serializer_class = QASerializer
    #filter_backends = (DjangoFilterBackend,)
#filter_fields = ('userKey','userId')


#画面と紐つかないAPI
def apitest(request):

    if "userKey" in request.GET:
        # query_paramが指定されている場合の処理
        param_value = request.GET.get("userKey")
        print("param_value:"+param_value)
        qas=[]
        for qa in QA.objects.filter(userKey=param_value).order_by('IdPerUser'):
            reply = qa.Answer
            if qa.Q1 != '':
                reply = reply + '<br>' + '1.' + qa.Q1
            if qa.Q2 != '':
                reply = reply + '<br>' + '2.' + qa.Q2
            if qa.Q3 != '':
                reply = reply + '<br>' + '3.' + qa.Q3
            if qa.Q4 != '':
                reply = reply + '<br>' + '4.' + qa.Q4
            if qa.Q5 != '':
                reply = reply + '<br>' + '5.' + qa.Q5
            qa_dict = OrderedDict([
                ('IdPerUser', qa.IdPerUser),
                ('Keyword', qa.Keyword),
                ('Answer', reply),
                ('URL', qa.URL),
                ('userId', qa.userId),
                ('Q1', qa.Q1),
                ('Q2', qa.Q2),
                ('Q3', qa.Q3),
                ('Q4', qa.Q4),
                ('Q5', qa.Q5),
                ('A1', qa.A1),
                ('A2', qa.A2),
                ('A3', qa.A3),
                ('A4', qa.A4),
                ('A5', qa.A5),

            ])

            qas.append(qa_dict)

        data = qas
        json_str = json.dumps(data, ensure_ascii=False)

        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8',status=None)
        print(response)
        return response

    else:
       # print("else")
        data = {'error':'error1234'}
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=None)
        return response