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
import logging

from ..models import *
from ..serializers import *

logger = logging.getLogger("server_log")

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
        logger.info(f"In UserSubmissionListView get: {request.data}")
        logger.info(f"Judge name: {request.user.username}")
        judge_username = request.user.username

        # Step 1: Get the latest submission ID for each (user, question) combination
        latest_submissions = UserSubmission.objects.values(
            'user_id', 'question_id'  # Grouping by user and question
        ).annotate(
            latest_id=models.Max('submission_id')  # Finding the max submission_id (latest one)
        )

        # Step 2: Extract the submission IDs from the query result
        submission_ids = [item['latest_id'] for item in latest_submissions]

        # Step 3: Retrieve the actual UserSubmission objects using the IDs
        submissions = UserSubmission.objects.filter(submission_id__in=submission_ids)

        serializer = UserSubmissionSerializer(
            submissions, many=True, context={"judge_username": judge_username}
        )  # Serialize as a list

        logger.info(f"Sending the following data for judgement (max 5):")
        # logger.info(serializer.data[0])
        
        temp = 0
        for row in serializer.data:
            # logger.info(
            #     f'{row["player_name"]} -> {row["question"]["question_id"]}'
            # )
            logger.info(row)
            temp += 1
            if temp >= 5:
                break
        
        logger.info("Data complete")

        return Response({"submissions": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, submission_id=None):
        logger.info(submission_id, request.data.get("score"), request.data.get("feedback"))        
        logger.info(request.data)
        try:
            # {'status': 'approved', 'score': 12, 'feedback': 'TEst judgement'}
            judge_username = request.user.username
            logger.info(f"Judge name in post: {request.user.username}")

            feedback = request.data.get("feedback")
            score = request.data.get("score")

            sub = UserSubmission.objects.get(submission_id=submission_id)
            
            judge_user = User.objects.get(username=judge_username)
            judge_obj = CustomUser.objects.get(user=judge_user)
            judgement = Judgment(user_submission=sub, remarks=feedback, score=score, judge=judge_obj)
            judgement.status = request.data.get("status")
            judgement.save()

        except Exception as e:
            logger.info(f"Error in judgement: {str(e)}")

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
    logger.info("In download_file")
    file_path = os.path.join("submissions", file_name)
    logger.info(f"File path: {file_path}")
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
