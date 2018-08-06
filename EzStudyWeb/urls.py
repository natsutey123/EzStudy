from django.urls import path
from . import views

urlpatterns = [

    path('', views.demopage, name="demo"),
    path('SignIn/', views.signIn, name="SignIn"),
    path('Homepage/', views.homepage, name="homepage"),
    path('LogOut/', views.LogOut, name="LogOut"),
    path('Ai/', views.ai, name="Ai"),
    path('Profile/', views.Profile, name="profile"),
    path('Register', views.register, name="register"),
    path('DoneSignUp/', views.DoneSignUp, name="DoneSignUp"),
    path('Library/', views.Library, name="library"),
    path('api/helloworld', views.helloWorld),
    path('api/hellopost', views.helloPost),
    path('api/hellojson', views.helloJson),
    path('udemy/showcourse', views.udemyShowCourse1)

]