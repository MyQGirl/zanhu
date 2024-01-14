# -*- coding:utf-8 -*-
# __author__ = '__Jack__'
from __future__ import unicode_literals
import uuid
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='publisher', verbose_name='用户')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='thread',
                               verbose_name='自关联')  # 动态跟评论的关联外键，因为动态跟评论在一张表里，所以这里是自关联
    context = models.TextField(verbose_name='动态内容')
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_news',
                                   verbose_name='点赞用户')
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '首页'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.context

    def switch_like(self, user):
        if user in self.user.all():
            self.liked.remove()  # 如果已经赞过，就取消赞
        else:
            self.user.add(user)

    #  返回记录的上级或者记录本身
    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return self

    #  给动态回复评论
    def reply_this(self, user, context):
        parent = self.get_parent()
        News.objects.create(
            user=user,
            context=context,
            reply=True,
            parent=parent,
        )

    #  parent是动态关联到评论的外键，thread反向查询，用动态的parent属性，查找说有的评论
    def get_thread(self):
        parent = self.get_parent()
        return parent.thread.all()

    #  获取该动态的评论数
    def comment_count(self):
        return self.get_thread().count()

    # 获取该评论的点赞数
    def count_likers(self):
        self.liked.count()

    # 获取点赞用户
    def get_likers(self):
        return self.liked.all()
