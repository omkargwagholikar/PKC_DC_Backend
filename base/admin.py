from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Question)
admin.site.register(UploadedFile)
admin.site.register(UserSubmission)
admin.site.register(Judgment)
admin.site.register(OldJudgment)