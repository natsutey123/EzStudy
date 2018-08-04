from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.http import JsonResponse
import json

config = {
    'apiKey': "AIzaSyBMBWE1mZLNMvlmy5xzFyQY3BttMkJjc7I",
    'authDomain': "ezstudywebapp.firebaseapp.com",
    'databaseURL': "https://ezstudywebapp.firebaseio.com",
    'projectId': "ezstudywebapp",
    'storageBucket': "ezstudywebapp.appspot.com",
    'messagingSenderId': "917055305787"
}

firebase = pyrebase.initialize_app(config)

aute = firebase.auth()
database = firebase.database()



def demopage(request):
    return render(request, "Firstpage.html")

def signIn(request):
    return render(request, "LogIn.html")

def register(request):
    return render(request, "SignUp.html")

def homepage(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = aute.sign_in_with_email_and_password(email, password)
    except:
        messages = "invalid users"
        return render(request, "LogIn.html", {"messg": messages})

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "Homepage.html", {"e": email})

def LogOut(request):
    auth.logout(request)
    return render(request, 'LogIn.html')

def DoneSignUp(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = aute.create_user_with_email_and_password(email, password)
        uid = user['localId']
        data = {"name": name, "status": "1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})

    return render(request, "Firstpage.html")

def ai(request):
    return render(request, "asistant.html")

def Profile(request):
    return render(request, "Profile Setting.html")

def Library(request):
    return render(request, "Library.html")

def helloWorld(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    return JsonResponse(data)

def helloPost(request):
    if request.method == 'GET':
        data = {
            'name': request.GET['name'],
            'location': request.GET['location'],
            'is_active': True,
            'count': 28
        }
        return JsonResponse(data)
    return JsonResponse({})

def helloJson(request):
    if request.method == 'GET':
        if request.body:
            json_data = json.loads(request.body)
        data = {
            'name': json_data['data']['name'],
            'location': json_data['data']['location'],
            'is_active': True,
            'count': 28
        }
        return JsonResponse(data)
    return JsonResponse({})

