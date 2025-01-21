# Generated by Django 5.1.3 on 2025-01-21 08:50

from django.db import migrations, models

import base.models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0007_remove_judgment_question_remove_judgment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadedfile",
            name="file_name",
            field=models.CharField(
                default="no name for old files", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="uploadedfile",
            name="subdirectory",
            field=models.CharField(
                choices=[
                    ("file_code", "file_code"),
                    ("file_documentation", "file_documentation"),
                    ("file_additional", "file_additional"),
                    ("Unspecified", "Unspecified"),
                ],
                default=("Unspecified", "Unspecified"),
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="uploadedfile",
            name="file",
            field=models.FileField(
                upload_to=base.models.UploadedFile.get_upload_path),
        ),
    ]
