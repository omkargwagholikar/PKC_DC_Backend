import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import *
from ..serializers import *


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
    ]
    return Response(routes)


class UserSubmissionListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        submissions = (
            UserSubmission.objects.all()
        )  # Retrieve all UserSubmission objects
        serializer = UserSubmissionSerializer(
            submissions, many=True
        )  # Serialize as a list
        return Response({"submissions": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, submission_id=None):
        print(submission_id, request.data.get(
            "score"), request.data.get("feedback"))
        # print(request.data)
        try:
            sub = UserSubmission.objects.get(submission_id=submission_id)
            judgement = Judgment(user_submission=sub,
                                 remarks="test", score=10.1)
            judgement.save()
        except Exception as e:
            print(f"Error in judgement: {str(e)}")

        return Response(
            {
                "status": "approved",
                "score": request.data.get("score"),
                "feedback": request.data.get("feedback"),
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
def download_file(request, file_name):
    # Path to the directory where your files are stored
    file_path = os.path.join("submissions", file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise Http404(f"The file {file_name} does not exist.")

    # Serve the file for download
    try:
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response
    except Exception as e:
        return Http404(f"Error while downloading file: {str(e)}")
