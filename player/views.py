from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from base.models import *
from rest_framework import status

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def solution(request):
    print(request.data)
    # Validate and decode the token
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(
            request.headers.get("Authorization").split(" ")[1]
        )
        user = jwt_authenticator.get_user(validated_token)
        print(f"> User: {user} submitting answer")
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

    # Get problem ID and validate the question
    problem_id = request.data.get("problemId")
    if not problem_id:
        return Response({"error": "Problem ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    question = get_object_or_404(Question, pk=problem_id)

    # Save uploaded files
    saved_files = []
    for key, file in request.FILES.items():        
        print(f"Saving {file.name} {key}")
        filename = file.name
        key = str(key).split("_")
        key.pop(-1)
        file_type = "_".join(key)
        file.name = f"{user}_{datetime.now()}_{file.name}"

        uploaded_file = UploadedFile(
            file=file,
            file_name=filename,
            subdirectory=file_type,
        )
        uploaded_file.save()
        saved_files.append(uploaded_file)

    # Create the UserSubmission entry
    try:
        print("Creating UserSubmission")
        user_submission = UserSubmission.objects.create(
            user=user,
            question=question,
            special_notes=request.data.get("description", "no notes"),
        )
        user_submission.files_submitted.set(saved_files)
        user_submission.save()
        print("Submission saved successfully")
    except Exception as e:
        print(f"Error in saving: {e}")
        return Response({"error": "Failed to save submission"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add file information to the response (optional)
    response_data = {
        "message": "Solution submitted successfully!",
        "submission_id": user_submission.submission_id,
        "files": [{"filename": f.file.name, "file_url": f.file.url} for f in saved_files],
    }

    return Response(response_data, status=status.HTTP_201_CREATED)
