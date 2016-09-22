from django.contrib import admin

from .models import User, Grade, Subject, subject_user

#admin.site.register(User)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(subject_user)