from django.shortcuts import render
import pyrebase
from django.contrib import auth


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

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))



