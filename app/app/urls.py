from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, re_path

from feed.views import index, view, signup, list_feed

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("signup", signup),
    path("signin", signup),
    re_path(r"^static/(?P<path>.+)", serve, kwargs={"insecure": True}),
    path("page/<int:page>/", list_feed),
    path("<str:forumid>", list_feed),
    path("<str:forumid>/page/<int:page>/", list_feed),
    path("<str:forumid>/<int:feed_id>/", view),
]
