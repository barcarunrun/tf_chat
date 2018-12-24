# coding: utf-8
"""
from rest_framework import serializers
from rest_framework import viewsets
from .models import QA
from django_filters import rest_framework as filters



class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = ['IdPerUser','Keyword','Answer','URL','userId','Q1','Q2','Q3','Q4','Q5','A1','A2','A3','A4','A5','userKey']


class QAFilter(filters.FilterSet):

    # フィルタの定義

    userKey = filters.CharFilter(userKey="test")
    class Meta:
        model = QA
        fields =['userKey']

"""


