import base64
import io
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notes
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
# Create your views here.

# notes - notes@123
# Tanmay - TanCodes@23


@login_required(login_url='loginPage')
def home(request):
    auth_user = request.user
    dis = Notes.objects.filter(user=request.user).order_by(
        '-last_updated')
    print("home-", len(dis))

    notes_queryset = Notes.objects.filter(user=request.user)
    notes_list = []

    for note in notes_queryset:
        note_text = note.body.replace('\r\n', '').strip()
        notes_list.append(note_text)

    print(type(notes_list))
    print(notes_list)

    # preprocess the text data
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          min_font_size=10).generate("".join(notes_list))

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    img_tag = graphic.decode('utf-8')

    context = {"auth_user": auth_user, "dis": dis,
               "total_notes": len(dis), "page": "OkNoted | HOME", "img_tag": img_tag}
    return render(request, "home.html", context)


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        pwd = request.POST.get("pwd")
        pwdfinal = request.POST.get("pwdfinal")
        print("this is user name", name)
        if not name or not email or not pwd or not pwdfinal:
            context = {"Error_message": True, "page": "OkNoted | SIGNUP"}
            return render(request, "signup.html", context)
        elif User.objects.filter(username=name).first():
            messages.error(request, "This username is already taken")
            print(User.objects.filter(username=name).first())
            return render(request, "signup.html", {"page": "OkNoted | SIGNUP"})
        else:
            if pwd == pwdfinal:
                users = User.objects.create_user(name, email, pwdfinal)
                users.save()
                context = {"success_signup": True}
                return render(request, "login.html", context)
            return render(request, "signup.html", {"pass_error": "pass_error", "page": "OkNoted | SIGNUP"})

    else:
        return render(request, "signup.html", {"page": "OkNoted | SIGNUP"})


def LoginPage(request):
    if request.method == "POST":
        login_username = request.POST.get('login_username')
        login_pass = request.POST.get('login_pass')

        if not login_username and not login_pass:
            context = {"Error_message": True, "page": "OkNoted | LOGIN"}
            return render(request, "login.html", context)
        else:
            user1 = authenticate(
                request, username=login_username, password=login_pass)

            if user1 is not None:
                login(request, user1)
                return redirect('home')
            else:
                context = {"Error_message_unauthorized": True,
                           "page": "OkNoted | LOGIN"}
                return render(request, "login.html", context)

    else:
        print("NOT A POST REQUEST")
        return render(request, "login.html", {"page": "OkNoted | LOGIN"})


def logoutPage(request):
    logout(request)
    return redirect("loginPage")


# > ADD notes
@login_required(login_url='loginPage')
def addNotes(request):

    if request.method == "POST":
        get_note = request.POST.get('get_note')

        if get_note:
            auth_user = request.user
            save_note = Notes.objects.create(user=auth_user, body=get_note)
            save_note.save()
            dis = Notes.objects.filter(
                user=request.user).order_by('-last_updated')
            print("-----------------", dis)

            notes_queryset = Notes.objects.filter(user=request.user)
            notes_list = []

            for note in notes_queryset:
                note_text = note.body.replace('\r\n', '').strip()
                notes_list.append(note_text)

            print(type(notes_list))
            print(notes_list)

                # preprocess the text data
            wordcloud = WordCloud(width=800, height=800,
                                background_color='white',
                                min_font_size=10).generate("".join(notes_list))

            plt.figure(figsize=(8, 8), facecolor=None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()

            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            graphic = base64.b64encode(image_png)
            img_tag = graphic.decode('utf-8')

            context = {"auth_user": auth_user,
                       "dis": dis, "total_notes": len(dis), "page": "OkNoted | HOME-added" , "img_tag":img_tag}
            return render(request, "home.html", context)
        else:
            return redirect("home")
    else:
        print("NOT A POST REQUEST")
        pass

# > Delete Notes ->


@login_required(login_url='loginPage')
def deleteNote(request, id):
    Notes.objects.get(pk=id).delete()
    return redirect("home")


@login_required(login_url='loginPage')
def updateNote(request, id):
    if request.method == "POST":
        auth_user = request.user

        get_txt = request.POST.get('txtarea')

        updated_data = Notes.objects.get(pk=id)
        updated_data.body = get_txt
        updated_data.save()

        dis = Notes.objects.filter(user=request.user).order_by(
            '-last_updated')
        print(dis)
        context = {"auth_user": auth_user, "dis": dis,
                   "total_notes": len(dis), "page": "OkNoted | HOME-updated"}
        return render(request, "home.html", context)
    else:
        print("not a post")


def ourstory(request):
    return render(request, "ourstory.html")
