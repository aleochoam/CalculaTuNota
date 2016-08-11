from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader

from .models import User, Grade, Subject, subject_user

def index(request):
    return render(request, "calc/index.html")

def createAccount(request):
    return render(request, "calc/createaccount.html")

def createAccount_submit(request):
    username = request.POST["username"]
    password = request.POST["password"]
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
    context = {
        "username" : user,
        "subjects" : [s.code for s in subjects]
    }
    return render(request, "calc/user.html", context)

def grades(request, user, subject):
    try:
        #user = User.objects.get(username=user)
        grades = Grade.objects.filter(username=user, subject=subject)
        average = getAverage(grades)
        faltante = getFaltante()
        context = {
            "username": user,
            "grades"  : grades,
            "average" : average,
        }
        return render(request, "calc/grades.html", context)
    except User.DoesNotExist:
        raise Http404("User doesn't exist")

def createUser(username, password):
    u = User(username=username, password=password)
    u.save()

"""
Funcion para calcular el promedio
"""
def getAverage(grades):
    sum = 0
    print(grades)
    for grade in grades:
        grade = str(grade).split();
        print(grade)
        sum += float(grade[0])*float(grade[1])/100

    return sum;

"""
Funcion que calcula la nota que necesita para ganar
"""
def getFaltante():
    pass
