from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.contrib import messages
from django.conf import settings
from .forms import UserLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from request.serializers import UserSerializer
from professor import views

from django.contrib.auth import logout



def login_view(request):

    log_in_form = UserLoginForm()
    context = {
        'log_in_form': log_in_form,
    }

    if request.method == 'POST':
        log_in_form = UserLoginForm(request.POST or None)
        if log_in_form.is_valid():
            username = log_in_form.cleaned_data.get("username")
            password = log_in_form.cleaned_data.get("password")
            data = {
                "username": username,
                "password": password
            }
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                serializer=UserSerializer(user)
                request.session['user'] = serializer.data

                if user.has_perm('auth.professor'):
                    print("es professor")
                    return redirect("/uvdomjudge/professor")

                elif user.has_perm('auth.administrator'):
                    print("es administrador")
                    return redirect("/uvdomjudge/administrator/")

            else:
                messages.error(request, "Invalid User.")

            print("no funciona return")


    return render(request, "login/login.html", context)





def logout_view(request):
    logout(request)
    return redirect("/uvdomjudge/")





