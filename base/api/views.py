import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from django.contrib import messages

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

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_judge = request.POST.get('is_judge', False) == 'on'
        is_player = request.POST.get('is_player', False) == 'on'

        # Basic validation checks
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('register')

        try:
            logger.info(f"username: {username} - email: {email} - password: {password} - is_judge: {is_judge} - is_player: {is_player}")
            user = User.objects.create_user(username=username, email=email, password=password)
            custom_user = CustomUser(
                user=user,
                is_judge = is_judge,
                is_player =is_player 
            )
            # Store custom data such as is_judge and is_player
            user.save()
            custom_user.save()
            
            logger.info("New user created")
            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to login page after successful registration
        except Exception as e:
            logger.exception(f"Error in user registerations: {e}")

            messages.error(request, f"Error: {e}")
            return redirect('register')
    
    return render(request, 'registration_form.html')

class UserSubmissionListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"In UserSubmissionListView get: {request.data}")
        logger.info(f"Judge name: {request.user.username}")
        judge_username = request.user.username
        judge_user = User.objects.filter(username=judge_username)
        try:
            judge_custom = CustomUser.objects.filter(user = judge_user.first()).first()
            if not judge_custom.is_judge:
                # raise
                logger.info(f"Player: {judge_username} trying to access judge panel")
                return Response({"submissions": []}, status=status.HTTP_200_OK)

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
            # submissions = submissions.exclude(user=judge_user)
            submissions = submissions.exclude(user_id=judge_user.first().id)


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
        
        except Exception as e:
            logger.info(f"There is an error: {str(e)}")
            return Response({"subm☻issions": []}, status=status.HTTP_200_OK)

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
