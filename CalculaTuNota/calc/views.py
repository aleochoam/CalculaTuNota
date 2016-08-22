from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader

from .models import User, Grade, Subject, subject_user

def index(request):
    return render(request, "calc/index.html")

def createAccount(request):
    return render(request, "calc/createaccount.html")

def createAccount_submit(request):
    username  = request.POST["username"]
    password  = request.POST["password"]
    password2 = request.POST["password2"]

    if password2 != password:
        return render(request, "calc/createaccount.html", {
            "error_message" : "Las contraseñas no coinciden"})
    else:
        try:
            user = User.objects.get(username=username)
            return render(request, "calc/createaccount.html", {
                "error_message": "El Usuario ya existe"})

        except User.DoesNotExist:
            createUser(username, password);
            return redirect("/calc/"+username)

def login(request):
    return render(request, "calc/login.html")

def login_submit(request):
    username = request.POST["username"]
    password = request.POST["password"]

    try:
        user = get_object_or_404(User, username=username)
        if user.password == password:
            return redirect("/calc/"+username)
        else:
            raise Exception("Contraseña equivocada")
    except (User.DoesNotExist, Exception):
        return render(request, "calc/login.html", {
            "error_message": "Usuario o contraseña invalido"})


def all_users(request):
    users = User.objects.all()
    #output = ', '.join([u.username for u in users])
    context = {
        "users": users,
    }
    return render(request, "calc/all_users.html", context)

def user(request, user):
    subjects = get_list_or_404(subject_user, username=user)
    subjects = [s.subject for s in subjects]
    context  = {
        "username" : user,
        "subjects" : [s.code for s in subjects]
    }
    return render(request, "calc/user.html", context)

def grades(request, user, subject):
    try:
        gradesDB    = Grade.objects.filter(username=user, subject=subject)
        notas       = [n.grade for n in gradesDB]
        porcentajes = [n.percentage for n in gradesDB]

        average     = getPromedio(notas, porcentajes)
        faltante    = getFaltante(notas, porcentajes)
        context     = {
            "username": user,
            "subject" : subject,
            "grades"  : gradesDB,
            "average" : average,
            "faltante": faltante,
            "acum"    : 100 - sum(porcentajes)
        }
        return render(request, "calc/grades.html", context)
    except User.DoesNotExist:
        raise Http404("User doesn't exist")

def addGrades(request, user, subject):
    return render(request, "calc/addGrades.html")

# def addGrades_submit(request,user,subject):



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