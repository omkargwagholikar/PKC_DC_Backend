from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from . import views

urlpatterns = [
    path("", views.getRoutes),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "submissions",
        views.UserSubmissionListView.as_view(),
        name="UserSubmissionListView",
    ),
    path(
        "submissions/<int:submission_id>/judge/",
        views.UserSubmissionListView.as_view(),
        name="submission-judge",
    ),
    # path(
    #     "download/submissions/<str:file_name>/",
    #     views.download_file,
    #     name="download_file",
    # ),
    re_path(r"^download/submissions/(?P<file_name>.+)/$", views.download_file, name="download_file")

]
