# -*- coding:utf-8 -*-
# __author__ = '__Jack__'
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from news.models import News


# Create your views here.

class NewsListView(LoginRequiredMixin, ListView):
    model = News
    paginate_by = 20
    template_name = "news/news_list.html"

    def get_queryset(self):
        return News.objects.filter(reply=False)
