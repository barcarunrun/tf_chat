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
    return render(request, 'QA.html')

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

class MyListView(ListView):
    model = QA


from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import \
    ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Memo
from .forms import MemoForm


class MemoListView(ListView):
    """
    メモを一覧表示
    テンプレートは、何も指定しないと モデル名_list.html が使われる
    ListView は、パジネーションもやってくれる
    """
    model = Memo
    paginate_by = 10  # 1ページに表示する件数


class MemoDetailView(DetailView):
    """
    1つのメモを詳細表示
    テンプレートは、何も指定しないと モデル名_detail.html が使われる
    """
    model = Memo


class MemoCreateView(CreateView):
    """
    メモ 新規作成
    完了ページを作成し、success_url で指定して表示してもいいが、
    django.contrib.messages の機能で、メッセージを保存して
    リストビューなんかに戻した時に表示するのも簡潔で良い。
    """
    model = Memo
    form_class = MemoForm
    success_url = reverse_lazy('memo_list')

    def form_valid(self, form):
        result = super(MemoCreateView,self).form_valid(form)
        messages.success(
            self.request, '「{}」を作成しました'.format(form.instance))
        return result


class MemoUpdateView(UpdateView):
    """
    メモ 更新
    """
    model = Memo
    form_class = MemoForm

    success_url = reverse_lazy('memo_list')

    def form_valid(self, form):
        result = super(MemoUpdateView,self).form_valid(form)
        messages.success(
            self.request, '「{}」を更新しました'.format(form.instance))
        return result


class MemoDeleteView(DeleteView):
    """
    メモ 削除
    デフォルトでは、get でリクエストすると確認ページ、
    post でリクエストすると削除を実行する、という動作。
    実際は、レコードを削除するのではなく有効フラグを消す(いわゆる論理削除)
    のケースが多いと思うので、そんな時はdeleteをオーバーライドしてその中で処理を書く。
    """
    model = Memo
    form_class = MemoForm

    success_url = reverse_lazy('memo_list')

    def delete(self, request, *args, **kwargs):
        result = super(MemoDeleteView,self).delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result

# coding: utf-8
import django_filters
from rest_framework import viewsets, filters

from .models import QA
from .serializer import QASerializer


class QAViewSet(viewsets.ModelViewSet):
    queryset = QA.objects.all()
    serializer_class = QASerializer
