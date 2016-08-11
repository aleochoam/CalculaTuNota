from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class User(models.Model):
    username = models.CharField(max_length=64, unique=True, primary_key=True)
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.username

@python_2_unicode_compatible
class Subject(models.Model):
    code        = models.CharField(max_length=10, unique=True, primary_key=True)
    subjectName = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code + " " + str(self.subjectName))

@python_2_unicode_compatible
class subject_user(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username) +" "+ str(self.subject)

@python_2_unicode_compatible
class Grade(models.Model):
    username   = models.ForeignKey(User, on_delete=models.CASCADE)
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade      = models.FloatField()
    percentage = models.FloatField()

    def __str__(self):
        return str(self.grade) + " " + str(self.percentage)
