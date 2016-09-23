import json

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import GradeSerializer, SubjectSerializer, SubjectUserSerializer
from .models import Grade, Subject, subject_user
from .forms import UserForm

def index(request):
    if request.user.is_authenticated:
        return redirect("user")
    else:
        return render(request, "calc/index.html")


def all_users(request):
    users = User.objects.all()
    return render(request, "calc/all_users.html", {"users": users})

def logout_view(request):
    logout(request)
    return redirect("/calc")

def user(request):
    if not request.user.is_authenticated:
        return redirect("/calc/login")

    subjects = subject_user.objects.filter(user = request.user.pk)
    #subjects = get_list_or_404(subject_user, username=user)

    subjects = [s.subject for s in subjects]
    context  = {
        "username" : request.user.username,
        "subjects" : [s.code for s in subjects]
    }
    return render(request, "calc/user.html", context)

def grades(request, subject):
   # try:
    gradesDB    = Grade.objects.filter(username_id=request.user.pk, subject=subject)
    notas       = [n.grade for n in gradesDB]
    porcentajes = [n.percentage for n in gradesDB]

    average     = getPromedio(notas, porcentajes)
    faltante    = getFaltante(notas, porcentajes)
    context     = {
        "username": request.user.username,
        "subject" : subject,
        "grades"  : gradesDB,
        "average" : average,
        "faltante": faltante,
        "acum"    : 100 - sum(porcentajes)
    }
    return render(request, "calc/grades.html", context)
    #except Exception:
     #   return render(request, "calc/grades.html", )

def addGrades(request, user, subject):
    return render(request, "calc/agregarNota.html")

def addGrades_submit(request,user,subject):

    userO    = User.objects.get(username = user)
    subjectO = Subject.objects.get(code = subject)

    grade = Grade(
        username   = userO,
        subject    = subjectO,
        grade      = float(request.POST["grade"]),
        percentage = float(request.POST["percentage"]))

    grade.save()

    return redirect("/calc/"+user+"/"+subject)

def addSubject(request, user):
    return render(request, "calc/addSubject.html")

def addSubject_submit(request, user):
    subject = request.POST["subject"]
    print("1" + subject + " " + user)
    try:
        subject = get_object_or_404(Subject, code = subject)
        user = get_object_or_404(User, username = user)
        print ("2" + subject + " " + user)
        newSubject = subject_user(username = user, subject = subject)
        newSubject.save()
        return redirect("/calc/"+user)

    except Http404:
        return render(request, "calc/addSubject.html", {
            "error_message": "El codigo de la materia no existe en la DB"})


class UserRegisterView(View):
    form_class = UserForm
    template_name = "calc/registration_form.html"

    def get(self, request):
        form = self. form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self. form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    #redirect a lista de notas
                    return redirect ("/calc/user")

        return render(request, self.template_name,
            {"form": form, "error_message": "error"})

class UserLogView(View):
    form_class = UserForm
    template_name = "calc/registration_form.html"

    def get(self, request):
        form = self. form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)

                #redirect a lista de notas
                return redirect ("/calc/user")

        return render(request, self.template_name,
                    {"form": form, "error_message": "error autenticando"})

"""
-------------------------------------------
             REST API
-------------------------------------------
"""
@api_view(['GET'])
def notaFaltante(request, user, subject):

    if request.method == 'GET':
        gradesDB    = Grade.objects.filter(username=user, subject=subject)
        notas       = [n.grade for n in gradesDB]
        porcentajes = [n.percentage for n in gradesDB]

        average     = getPromedio(notas, porcentajes)
        faltante    = getFaltante(notas, porcentajes)

        return Response({"faltante": faltante, "promedio": average})

class GradeList(APIView):
    def get(self, request, user, subject):
        gradesDB = Grade.objects.filter(username=user, subject=subject)
        serializer = GradeSerializer(gradesDB, many=True)
        print ("DEBUG " + str(serializer.data))
        return Response(serializer.data)

    # Por Probar
    def post(self, request, format=None):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
Mostrar Todas las materias en las que está inscrito, o inscribir una nueva
"""
class UserSubjectList(APIView):

    def get(self, request, user, format=None):
        subjects   = subject_user.objects.filter(username = user)
        serializer = SubjectUserSerializer(subjects, many = True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SubjectUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def createUser(username, password):
    u = User(username=username, password=password)
    u.save()


def getPromedio(notas, porcentajes):
    porcentajeNotas = []
    porcentajeTotal = sum(porcentajes)

    for porcentaje in porcentajes:
        porcentajeDef = porcentaje/porcentajeTotal*100
        porcentajeNotas.append(porcentajeDef)

    final = 0
    for i in range(len(notas)):
        final += notas[i] * (porcentajeNotas[i]/100)
    return final

"""
Funcion que calcula la nota que necesita para ganar
"""
def getFaltante(notas, porcentaje):
    acum = 0
    percent = 0
    for i in range(len(notas)):
        temp = notas[i] * (porcentaje[i]/100)
        acum = acum + temp
        percent = percent + porcentaje[i]
    if (percent == 100):
        return acum
    elif (percent < 100):
        percent1 = (100 - percent)/100
        acum = 3 - acum
        final = acum/percent1
        return final
    else:
        return "ERROR!"