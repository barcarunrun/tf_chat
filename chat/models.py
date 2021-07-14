# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from six import python_2_unicode_compatible
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime
from django.utils import timezone

# from django.contrib.auth import get_user_model
# User = get_user_model()
# Create your models here.


class AuthUserManager(BaseUserManager):
    def create_user(self, username, password):
        """
        ユーザ作成
        :param userId: ユーザID
        :param password: パスワード
        :return: AuthUserオブジェクト
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(username=username,
                          password=password,
                          )
        user.adminFlag = False

        # user.set_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        スーパーユーザ作成

        :param username: ユーザID
        :param password: パスワード
        :return: AuthUserオブジェクト
        """
        user = self.create_user(username=username,
                                password=password
                                )
        user.is_superuser = True
        user.is_staff = False
        user.LoginTimes = datetime.now()
        user.set_password(password)
        user.adminFlag = True
        user.save(using=self._db)
        return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
    """
    ユーザ情報を管理する
    """
    class Meta:
        verbose_name = 'ユーザ'
        verbose_name_plural = 'ユーザ'

    username = models.CharField(verbose_name='ユーザ名称',
                                unique=True,
                                max_length=30)

    adminFlag = models.BooleanField(verbose_name='管理者フラグ',
                                    default=False)
    # LoginTimes=models.BigIntegerField()
    recent_login_date = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    author = models.CharField(max_length=200, blank=True, null=True)
    userpassword = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(('staff status'), default=False)
    objects = AuthUserManager()

    def __str__(self):
        return self.username


class Log(models.Model):
    userId = models.CharField(max_length=30)
    DateTime = models.DateTimeField(auto_now_add=True)
    Question = models.CharField(max_length=200)
    AnswerNo = models.BigIntegerField()
    Answer = models.CharField(max_length=200)
    Withdrawal = models.BooleanField(default=False)
    ScreenId=models.CharField(max_length=200)


CHOICE = {
    (False, 'テスト'),
    (True, '公開')
}


class QA(models.Model):
    is_public = models.BooleanField(choices=CHOICE, default=False)
    Keyword = models.CharField(max_length=100, blank=True, null=True)
    Answer = models.CharField(max_length=200)
    URL = models.URLField(max_length=300)
    #NextAnswerNo = models.BigIntegerField()
    #Question = models.CharField(max_length=200)
    userId = models.CharField(verbose_name='ユーザID',
                              unique=False,
                              max_length=30)
    Q1 = models.CharField(max_length=10, blank=True, null=True)
    Q2 = models.CharField(max_length=10, blank=True, null=True)
    Q3 = models.CharField(max_length=10, blank=True, null=True)
    Q4 = models.CharField(max_length=10, blank=True, null=True)
    Q5 = models.CharField(max_length=10, blank=True, null=True)
    A1 = models.CharField(max_length=10, blank=True, null=True)
    A2 = models.CharField(max_length=10, blank=True, null=True)
    A3 = models.CharField(max_length=10, blank=True, null=True)
    A4 = models.CharField(max_length=10, blank=True, null=True)
    A5 = models.CharField(max_length=10, blank=True, null=True)
    IdPerUser = models.IntegerField()
    userKey = models.CharField(max_length=100)

class AdminFlag(models.Model):
    userId = models.CharField(max_length=30)
    userKey = models.CharField(max_length=100)
    adminUser = models.CharField(max_length=30)