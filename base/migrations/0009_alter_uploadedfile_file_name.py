# Generated by Django 5.1.3 on 2025-01-21 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0008_uploadedfile_file_name_uploadedfile_subdirectory_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploadedfile",
            name="file_name",
            field=models.TextField(),
        ),
    ]
