from django.urls import path
from . import views

urlpatterns = [

    path('', views.demopage),
    path('SignIn/', views.signIn, name="SignIn"),
    path('Homepage/', views.homepage, name="homepage"),
    path('LogOut/', views.LogOut, name="LogOut"),
    path('Ai/', views.ai, name="Ai"),
    path('Profile/', views.Profile, name="profile"),
    path('Register', views.register, name="register"),
    path('DoneSignUp/', views.DoneSignUp, name="DoneSignUp"),
    path('Library/', views.Library, name="library")

]