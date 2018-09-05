# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime


# Create your models here.

class AuthUserManager(BaseUserManager):
    def create_user(self, userId, password):
        """
        ユーザ作成

        :param userId: ユーザID
        :param password: パスワード
        :return: AuthUserオブジェクト
        """
        if not userId:
            raise ValueError('Users must have an username')

        user = self.model(username=userId,
                          password=password,
                          )
        user.adminFlag = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, password):
        """
        スーパーユーザ作成

        :param userId: ユーザID
        :param password: パスワード
        :return: AuthUserオブジェクト
        """
        user = self.create_user(username=userId,
                                password=password
                                )
        user.is_superuser = True
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

    username = models.CharField(verbose_name='ユーザID',
                                unique=True,
                                max_length=30)

    adminFlag = models.BooleanField(verbose_name='管理者フラグ',
                                    default=False)
    LoginTimes=models.BigIntegerField()
    recent_login_date = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    objects = AuthUserManager()

    def __str__(self):
        return self.username


class Log(models.Model):
    userId = models.CharField(max_length=30)
    DateTime = models.DateTimeField(auto_now_add=True)
    Question=models.CharField(max_length = 200)
    AnswerNo = models.BigIntegerField()
    Answer = models.CharField(max_length=200)
    Withdrawal=models.BooleanField(default=False)


class QA(models.Model):
    Keyword = models.CharField(max_length=100)
    Answer = models.CharField(max_length=200)
    URL=models.URLField(max_length=300)
    NextAnswerNo = models.BigIntegerField()
    Question = models.CharField(max_length=200)
    userId = models.CharField(verbose_name='ユーザID',
                                unique=False,
                                max_length=30)

class Item(models.Model):
    name = models.CharField(max_length=20)
    value = models.IntegerField()


class Memo(models.Model):
    """
    メモモデル。実質、件名と本文のみ。
    """
    subject = models.CharField(
        verbose_name='件名',
        max_length=100,
        default='',
        blank=True
    )

    body = models.TextField(
        verbose_name='本文',
        default='',
        blank=True
    )

    # created: auto_now_add を指定すると、作成日時を自動保存する
    created = models.DateTimeField(
        auto_now_add=True
    )

    # updated: auto_now を指定すると、更新日時を自動保存する
    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.subject





