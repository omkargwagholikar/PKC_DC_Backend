from django.contrib.auth.models import User
from rest_framework import serializers
import logging
from .models import *

logger = logging.getLogger("seralizer_log")


# Serializer for UploadedFile model
class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = [
            "id",
            "file",
            "uploaded_at",
            "file_name",
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

    status = serializers.SerializerMethodField()  # Dynamically fetch status



    def get_status(self, obj):
        judge_username = self.context.get("judge_username")  # Get judge from context
        logger.info(f"Judge: {judge_username}, Submission id: {obj.submission_id}")

        if not judge_username:
            return "pending"
                
        # Get the latest judgment status if it exists, else return "pending"
        # judgment = Judgment.objects.filter(user_submission=obj).first()
        judge_user = User.objects.get(username = judge_username)
        judge = CustomUser.objects.get(user = judge_user)
        judgment = Judgment.objects.filter(user_submission=obj, judge=judge).first()

        return judgment.status if judgment else "pending"    

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
