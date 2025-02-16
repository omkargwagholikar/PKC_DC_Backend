from django.contrib.auth.models import User
from django.db import models


# Custom User model extending the default User model
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_judge = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# Model for Question
class Question(models.Model):
    DIFFICULTY_LEVELS = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    question_id = models.AutoField(primary_key=True)
    domain = models.CharField(max_length=255)
    problem_title = models.TextField()
    problem_statement = models.TextField()
    difficulty_level = models.CharField(
        max_length=10, choices=DIFFICULTY_LEVELS)

    def __str__(self):
        return f"Question {self.question_id}: {self.domain}"


# Model for User Submission and file tracking
class UploadedFile(models.Model):
    SUBDIRECTORY_CHOICES = [
        ("file_code", "file_code"),
        ("file_documentation", "file_documentation"),
        ("file_additional", "file_additional"),
        ("Unspecified", "Unspecified"),
    ]

    subdirectory = models.CharField(
        max_length=100,
        choices=SUBDIRECTORY_CHOICES,
        default=SUBDIRECTORY_CHOICES[3],  # Default is 'Unspecified'
    )

    def get_upload_path(self, filename):
        return f"submissions/{self.subdirectory}/{filename}"

    file = models.FileField(upload_to=get_upload_path, max_length=500)
    file_name = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class UserSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    files_submitted = models.ManyToManyField(
        UploadedFile, related_name="submissions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    special_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission {self.submission_id} by {self.user.username}"


# Model for Judgments
class Judgment(models.Model):
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE)
    
    judge = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    remarks = models.TextField()
    score = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    def __str__(self):
        return f"Judgment for Submission {self.user_submission.submission_id}"
