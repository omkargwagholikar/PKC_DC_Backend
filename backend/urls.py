from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("base.api.urls")),
    path("player/", include("player.urls")),
    path("api/player/", include("player.urls")),
    path("judge/", include("judge.urls")),
]
