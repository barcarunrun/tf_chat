# coding: utf-8

from rest_framework import serializers

from .models import QA


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = ('id','Keyword', 'Answer','URL','NextAnswerNo','Question')
