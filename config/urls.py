from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from django.views.generic import TemplateView
from django.views import defaults as default_views

from news.views import NewsListView

# 0.0.0.0:8000/
urlpatterns = [
                  # 首页
                  path("", NewsListView.as_view, name="home"),
                  # User management 用户管理
                  path("users/", include("zanhu.users.urls", namespace="users")),
                  #  动态
                  path("news/", include("zanhu.news.urls", namespace="news")),
                  path("accounts/", include("allauth.urls")),

                  # Your stuff: custom urls includes go here
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
