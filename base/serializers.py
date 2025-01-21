from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


# Serializer for UploadedFile model
class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = [
            "id",
            "file",
            "uploaded_at",
        ]  # Adjust fields based on UploadedFile's attributes


# Serializer for Question model
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["question_id", "domain", "problem_title", "difficulty_level"]


# Serializer for UserSubmission model
class UserSubmissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="submission_id")
    player_name = serializers.CharField(
        source="user.username"
    )  # Access 'username' of related 'user'
    submitted_at = serializers.DateTimeField(
        source="timestamp"
    )  # Rename 'timestamp' to 'submitted_at'
    score = serializers.FloatField(
        allow_null=True, default=None
    )  # Include null value for score
    feedback = serializers.CharField(
        allow_null=True, default=None
    )  # Include null value for feedback
    files = UploadedFileSerializer(
        many=True, read_only=True, source="files_submitted"
    )  # Map to files_submitted  # Nested serializer for files
    question = (
        QuestionSerializer()
    )  # Use the QuestionSerializer for detailed representation

    class Meta:
        model = UserSubmission
        fields = [
            "id",
            "player_name",
            "submitted_at",
            "status",
            "score",
            "feedback",
            "files",
            "question",
            "special_notes",
        ]
