from django.conf import settings
from rest_framework import status
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import *
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',        
    ]
    return Response(routes)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def solution(request):
    # Validate and decode the token
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(request.headers.get("Authorization").split(" ")[1])
        user = jwt_authenticator.get_user(validated_token)
        print(f"User: {user} submitting answer")
    except Exception as e:
        return Response({"error": "Invalid or expired token"}, status=401)
    
    # Save uploaded files
    problem_id = request.data.get("problemId")
    save_directory = os.path.join(settings.MEDIA_ROOT, "submission", problem_id)
    os.makedirs(save_directory, exist_ok=True)
    
    for key, file in request.FILES.items():
        file_path = os.path.join(save_directory, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    
    return Response({"message": "Solution submitted successfully!"})