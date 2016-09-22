from rest_framework import serializers
from calc.models import Subject, Grade, subject_user

"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
"""

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('code', 'subjectName')

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('grade', 'percentage')

class SubjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = subject_user
        fields = ('subject',)
