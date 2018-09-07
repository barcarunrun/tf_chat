# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from models import Log, QA
import sys, os
import base64
import logging
from datetime import datetime
from django.http import HttpResponse, JsonResponse

import uuid, tempfile

from django.shortcuts import render, redirect
import json
from collections import OrderedDict

from django.shortcuts import render

from django.shortcuts import render, redirect

import forms
from extra_views import CreateWithInlinesView, InlineFormSet

from django.views.generic import ListView

from .forms import ItemFormSet2,ItemForm
from django.core.cache import cache

from django import forms
from django.forms import formsets
from django.forms import models



from django.utils import six

# Create your views here.

def index(request):
    if request.method != 'POST':

        data = {'id': 1, 'name': {'name1':'hoge','name2':'huga'}}
        request.session['json'] = data
        return render(request, 'Chat.html')

    print (1)
    print ('request.POST:' + request.POST['userId'])
    insert_data = Log(userId=request.POST['userId'],
                      Question=request.POST['Question'],
                      AnswerNo=request.POST['AnswerNo'],
                      Answer=request.POST['Answer'],
                      Withdrawal=request.POST['Withdrawal']
                      )

    insert_data.save()

    return render(request, 'Chat.html')


def log(request):
    return render(request, 'Log.html')

def topPage(request):
    return render(request, 'TopPage.html')

def qa(request):
    if request.method != 'POST':
        formset = ItemFormSet2
        return render(request, 'QA.html', {'formset': formset,})

    cache.clear()
    insertNum = int(request.POST['buttom']) - 1  # formは０からはじまるため
    print ('buttom:' + request.POST['buttom'])
    if request.POST['form-'+str(insertNum)+'-id']!='':
        serachNum=int(request.POST['form-'+str(insertNum)+'-id'])
        serachObj=QA.objects.filter(id=str(serachNum))

   # print ('serachObj:' + str(serachObj.values()))
    #print ('serachObj.count():'+str(serachObj.count()))

    if request.POST['form-'+str(insertNum)+'-id']=='':
        print ('hogehoge')
        insert_data = QA(Keyword =request.POST['form-'+str(insertNum)+'-Keyword'],
                         Answer =request.POST['form-'+str(insertNum)+'-Answer'],
                         URL=request.POST['form-'+str(insertNum)+'-URL'],
                         userId='user',
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
                         IdPerUser=insertNum-1
        )
        insert_data.save()
    else :
        print ('hugahuga')
        serachObj = QA.objects.get(id=str(serachNum))
        serachObj.Keyword = request.POST['form-'+str(insertNum)+'-Keyword']
        serachObj.Answer = request.POST['form-' + str(insertNum) + '-Answer']
        serachObj.URL = request.POST['form-' + str(insertNum) + '-URL']
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

    num = 30 - QA.objects.filter(userId='user').count()
    formset = formsets.formset_factory(ItemForm, extra=num, formset=models.BaseModelFormSet)(queryset=QA.objects.filter(userId='user'))
    formset.model = QA
    return render(request, 'QA.html', {'formset': formset })

def setting(request):
    return render(request, 'Setting.html')


def test(request):
    """ModelFormSetを使うと一括データ編集のフォームを簡単に作れる
    """
    formset = forms.ItemForm(request.POST or None)
    f=forms.ItemForm(request.POST or None)
    if formset.is_valid():
        # BaseModelFormSetを継承している場合はsaveメソッドを呼んで保存できる
        formset.save()
        return redirect('test')
    return render(request, 'test.html', {'formset': formset,'profile_form':f})


# coding: utf-8
import django_filters
from rest_framework import viewsets, filters

from .models import QA
from .serializer import QASerializer,QAFilter



class QAViewSet(viewsets.ModelViewSet):
    queryset = QA.objects.filter(userId='user').order_by('IdPerUser')
    serializer_class = QASerializer
