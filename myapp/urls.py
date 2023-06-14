
from django.contrib import admin
from django.urls import path
from myapp.views import home, signup, LoginPage, logoutPage, addNotes, deleteNote, updateNote, ourstory

urlpatterns = [
    # related authentication
    path("", signup, name="signup"),
    path("home/", home, name="home"),
    path("login/", LoginPage, name="loginPage"),
    path("logout/", logoutPage, name="logout"),

    path("ourstory/", ourstory, name='ourstory'),

    # related notes
    path("addnotes/", addNotes, name="addNotes"),
    path("deleteNote/<int:id>", deleteNote),
    path("updateNote/<int:id>", updateNote, name="updateNote"),
]
