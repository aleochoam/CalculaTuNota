from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader

from .models import User, Grade
# Create your views here.
def index(request):
    return render(request, "calc/index.html")

def createAccount(request):
    return HttpResponse("Creando Cuenta")

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

    except UserDoesNotExist:
        return render(request, "calc/login.html", {
            "error_message": "Usuario o contraseña invalido"})


def all_users(request):
    users = User.objects.all()
    output = ', '.join([u.username for u in users])
    context = {
        "users": users,
    }
    return render(request, "calc/all_users.html", context)

def user(request, user):
    try:
        #user = User.objects.get(username=user)
        grades = Grade.objects.filter(username=user)
        average = getAverage(grades)
        faltante = getFaltante()
        context = {
            "username": user,
            "grades"  : grades,
            "average" : average,
        }
        return render(request, "calc/user.html", context)
    except User.DoesNotExist:
        raise Http404("User doesn't exist")

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
