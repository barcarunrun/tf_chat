from django import forms
from django.forms import formsets
from django.forms import models
from .models import QA
from django.forms import modelformset_factory
from django.forms import formset_factory
from django.core.cache import cache

#ItemFormSet =forms.modelformset_factory(QA, extra=1)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class ItemForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = '__all__'



num=30-QA.objects.filter(userId='user').count()
#num=0
def create(user):
    ItemFormSet2 = formsets.formset_factory(ItemForm, extra=num, formset=models.BaseModelFormSet)(queryset=QA.objects.filter(userId=user))
    ItemFormSet2.model = QA
    return ItemFormSet2

