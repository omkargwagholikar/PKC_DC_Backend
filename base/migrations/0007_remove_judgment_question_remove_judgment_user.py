# Generated by Django 5.1.3 on 2025-01-15 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_remove_usersubmission_feedback_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="judgment",
            name="question",
        ),
        migrations.RemoveField(
            model_name="judgment",
            name="user",
        ),
    ]
