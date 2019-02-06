from django import forms
from django.forms import formsets
from django.forms import models
from .models import QA
from django.forms import modelformset_factory
from django.forms import formset_factory
from django.core.cache import cache

# ItemFormSet =forms.modelformset_factory(QA, extra=1)
from django.contrib.auth.forms import UserCreationForm



class SignUpForm(UserCreationForm):
    username = forms.CharField()
    userpassword = forms.CharField()
    author = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ItemForm(forms.ModelForm):
    class Meta:
        model = QA
        widgets = {
            'is_public': forms.RadioSelect
        }
        fields = '__all__'





def create(user):
    num = 100 - QA.objects.filter(userId=user).count()
    print num
    ItemFormSet2 = formsets.formset_factory(ItemForm, extra=num, formset=models.BaseModelFormSet)(
        queryset=QA.objects.filter(userId=user))
    ItemFormSet2.model = QA
    return ItemFormSet2
