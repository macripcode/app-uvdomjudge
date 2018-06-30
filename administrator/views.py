import json
import os
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from .forms import CreateUserForm
from request.clients import get_periods
from request.clients import delete_period_courses
from request.clients import delete_period_containers
from request.clients import delete_period
from request.clients import create_user



def administrator_profile(request):
    create_user_form = CreateUserForm()
    academic_periods = json.loads((get_periods()).decode('utf-8'))
    print("academics periods")
    print(type(academic_periods))
    print(academic_periods)
    print("academics periods")

    context = {
        'create_user_form' : create_user_form,
        'academic_periods' : academic_periods,
    }

    if request.method == 'POST':

        create_user_form = CreateUserForm(request.POST or None)

        if create_user_form.is_valid():

            type_user = create_user_form.cleaned_data.get("type_user")
            print("el tipo de dato de usuario es")
            print(type(type_user))
            username = create_user_form.cleaned_data.get("username")
            first_name = create_user_form.cleaned_data.get("first_name")
            last_name = create_user_form.cleaned_data.get("last_name")
            email = create_user_form.cleaned_data.get("email")
            id = create_user_form.cleaned_data.get("id")
            password = create_user_form.cleaned_data.get("password")

            #-------Creating User-------->
            user = User(
                username = username,
                first_name=first_name ,
                last_name=last_name,
                email=email,
                id=id
            )
            user.set_password(password)
            user.save()

            #------Giving permissions--->

            if type_user == "1":
                permission_administrator = Permission.objects.get(name='administrator')
                user.user_permissions.add(permission_administrator)
                user.save()

            if type_user == "2":
                permission_professor = Permission.objects.get(name='professor')
                user.user_permissions.add(permission_professor)
                user.save()

            # ------Creating token--->
            user = User.objects.get(id=id)
            token = Token.objects.create(user=user)

            #------Creating info to send api
            data_user = {
                "id": id,
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "token": token.key
            }

            data_str = json.dumps(data_user)
            print("data str")
            print(data_str)
            data_enc = data_str.encode('utf-8')
            print("data enc")
            print(data_enc)


            print(data_user)
            response = create_user(data_enc)
            print(response)

            if user.has_perm('auth.administrator') or user.has_perm('auth.professor'):
                return redirect("/uvdomjugde/administrator/created_user")
            else:
                return redirect("/uvdomjugde/administrator/fail_user")

        else:
            print(create_user_form.errors)

    return render(request, "profile/administrator_profile.html", context)


def create_backups(request):

    #quitar periodo del api cuando se realice el backups

    response ={}
    data = request.GET['selecteditems'].split(",")
    print(type(data))
    print(data)

    # path of folder of docker's volumes
    folder_docker_volumes = "/var/lib/docker/volumes/"
    # path of folder where period's backups will be stored
    folder_periods_backups = "/home/macripco/periods_backups"


    for i in data:
        #crear directorio de almacenamiento por semestre
        query1="cd "+folder_docker_volumes+" && mkdir " + folder_periods_backups + "/" + i +" && chmod -R 777 " + folder_periods_backups + "/" + i
        #comprimir todas los backups que corresponden a ese periodo y eliminarlos
        query2="cd "+folder_docker_volumes+" && for folder in $(ls -d "+i+"*); do tar -cvf $folder"+".tar"+" $folder && rm -R $folder ;done"
        # copiar los .tar a la carpeta semestral y eliminarlos
        query3="cd "+folder_docker_volumes+" && for folder in $(ls *.tar); do cp $folder " + folder_periods_backups +"/"+ i +" && rm $folder; done"

        os.system(query1)
        os.system(query2)
        os.system(query3)

        response1 = delete_period_courses(i).decode('utf-8')

        print(type(response1))
        print(response1)

        if response1 == '200':
            response2 = delete_period_containers(i).decode('utf-8')
            print(type(response2))
            print(response2)
            if response2 == '200':
                response3=delete_period(i).decode('utf-8')
                print(type(response3))
                print(response3)
                if response3 == '200':
                    response['message'] = "Backups has been created successfully."
                else:
                    response['message'] = "Backups could not be created."

            else:
                response['message'] = "Backups could not be created."

        else:
            response['message'] = "Backups could not be created."

    print(response)
    return JsonResponse(response)









def page_created_user(request):
    return render(request, "profile/created_user.html")

def page_fail_user(request):
    return render(request, "profile/fail_created_user.html")


def created_backups_success(request):
    return render(request, "profile/created_backups_success.html")

def created_backups_fail(request):
    return render(request, "profile/created_backups_fail.html")



