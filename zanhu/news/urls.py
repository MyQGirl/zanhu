from django.urls import path

from news import views

app_name = "news"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="list"),
]
