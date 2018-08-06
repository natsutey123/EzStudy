from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.http import JsonResponse,HttpResponse
import json
import requests

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import  os

from flask import Flask
from flask import request
from flask import make_response

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

    return render(request, "Library.html",)

# def helloWorld(request):
#     data = {
#         'name': 'Vitor',
#         'location': 'Finland',
#         'is_active': True,
#         'count': 28
#     }
#     return JsonResponse(data)
#
# def helloPost(request):
#     if request.method == 'GET':
#         data = {
#             'name': request.GET['name'],
#             'location': request.GET['location'],
#             'is_active': True,
#             'count': 28
#         }
#         return JsonResponse(data)
#     return JsonResponse({})
#
# def helloJson(request):
#     if request.method == 'GET':
#         if request.body:
#             json_data = json.loads(request.body)
#         data = {
#             'name': json_data['data']['name'],
#             'location': json_data['data']['location'],
#             'is_active': True,
#             'count': 28
#         }
#         return JsonResponse(data)
#     return JsonResponse({})
#
# def udemyShowCourse1(request):
#     requirement = {'ordering': 'most-reveiwed'}
#     r_showcourse = requests.get('https://www.udemy.com/api-2.0/courses/?ordering=most-reviewed&page=1&page_size=1',
#                                 auth=('EvBrZjvwgbY6iXWujMJE1qnNrZTmaOnDVpC57Sl9', 'neaBg8yIevDFSIXZpKZix6QyksQ2707REavzABZ507HjLtlzKKiBdvoqyvVLXWb3DptFnj7D6fGTk3YUbpc1Qtaj6gvMm24S63lSQlq4qiMbzCwiI3tKtOoG6C22IKze'),
#                                 data=requirement)
#     content = r_showcourse.json()
#     content_data = content['results']
#     content_result = content_data[00]
#     course_urls = "https://www.udemy.com" + content_result['url']
#     course_title = content_result['title']
#     course_image = content_result['image_480x270']
#     return HttpResponse(course_image)


app = Flask(__name__)
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req,indent=4))

    res = processRequest(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
def processRequest(req):
    print("here I am....")
    print("starting processRequest...",req.get("queryResult").get("action"))
    if req.get("queryResult").get("action") != "udemySearchCourse":
        print("Pls check action name in DialogFlow")
        return {}
    print("111111111111")
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    print("1.5 1.5 1.5")
    yql_query = makeYqlQuery(req)
    print("2222222222")
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    print("3333333333")
    print(yql_url)
    result = urlopen(yql_url).read()
    data = json.loads(result)
    # for some the line above gives an error and hence decoding to utf-8 might help
    # data = json.loads(result.decode('utf-8'))
    print("44444444444")
    print(data)
    res = udemySearchCourses(data)
    return res

def makeYqlQuery(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    search = parameters.get("search")
    price = parameters.get("price")
    instructional_level = parameters.get("instructional_level")

    if search & price & instructional_level is None:
        return None
    return {}


def udemySearchCourses(data):

    requirement = data.get('query')
    r_searchcourse = requests.get('https://www.udemy.com/api-2.0/courses/',
                               auth=('EvBrZjvwgbY6iXWujMJE1qnNrZTmaOnDVpC57Sl9', 'neaBg8yIevDFSIXZpKZix6QyksQ2707REavzABZ507HjLtlzKKiBdvoqyvVLXWb3DptFnj7D6fGTk3YUbpc1Qtaj6gvMm24S63lSQlq4qiMbzCwiI3tKtOoG6C22IKze'),
                                  params=requirement)
    content = r_searchcourse.json()
    content_data = content['results']
    content_result = content_data[00]
    course_urls = "https://www.udemy.com" + content_result['url']
    course_title = content_result['title']

    speech = "This is your best course" + '\n' + course_title + '\n' + course_urls

    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        "source": "UdemyApi"
    }

if __name__ == '__main__':


    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')