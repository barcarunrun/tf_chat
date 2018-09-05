from django import forms
from django.forms import formsets
from django.forms import models
from .models import QA
from django.forms import modelformset_factory
from django.forms import formset_factory


#ItemFormSet =forms.modelformset_factory(QA, extra=1)


class ItemForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = "__all__"

ItemFormSet2 = formsets.formset_factory(ItemForm, extra=3, formset=models.BaseModelFormSet)
ItemFormSet2.model = QA


class ProfileForm(forms.Form):

    name = forms.CharField()
    age = forms.IntegerField()


from .models import Memo


class MemoForm(forms.ModelForm):

    class Meta:
        model = Memo
        fields = ['subject', 'body']