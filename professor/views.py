from django.shortcuts import render
from .forms import CreateCourseForm
from .forms import ConfigProfileForm
from request.serializers import CourseSerializer
from request.clients import create_course
from request.clients import get_image_detail
from request.clients import run_container
from request.clients import check_period
from request.clients import create_period
from request.clients import get_data_container
from request.clients import create_container
from request.clients import check_course
from request.clients import get_courses_by_professor
from request.clients import get_container
from request.clients import set_pass_professor


from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.views.static import serve

import os
import json


def professor_profile(request):

    # ------- get courses by professor ------------>
    user = request.user
    id_professor = str(user.id)
    print(id_professor)
    courses_professor_enc =get_courses_by_professor(id_professor)

    courses_professor_str = (courses_professor_enc.decode('utf-8')).replace('Ã³','ó')
    courses_professor=json.loads(courses_professor_str)

    # ------- assigning url to each course ------------>

    for course in courses_professor:
        id_course=course['id_course']
        container_enc=get_container(id_course)
        container_str=container_enc.decode('utf-8')
        container=json.loads(container_str)
        port_80_container=container['port_number_80_container']
        url='http://localhost:'+port_80_container+'/domjudge/public/login.php'
        course['url']=url



    create_course_form = CreateCourseForm()
    create_course_form.fields['group_course'].widget.attrs = {
        'id': 'input_group_course',
        'data-length':'3',
        'type':'number',
        'min':'1',
        'max':'100',
        'class': 'validate',
    }
    create_course_form.fields['professor_course'].widget.attrs = {'id': 'input_professor_course',}
    config_profile_form = ConfigProfileForm()

    context={
        'courses_professor': courses_professor,
        'create_course_form': create_course_form,
        'config_profile_form': config_profile_form,
    }

    print(courses_professor)

    if request.method == 'POST':
        create_course_form = CreateCourseForm(request.POST)
        #config_profile_form = ConfigProfileForm(request.POST)

        if create_course_form.is_valid():
            print("es formulario de curso")
            code_course = create_course_form.data['code_course']
            name_course = create_course_form.data['name_course']
            credits_course = create_course_form.data['credits_course']
            professor_course = create_course_form.data['professor_course']
            group_course = create_course_form.data['group_course']
            period_course = create_course_form.data['period_course']
            year_course = create_course_form.data['year_course']
            programming_language = create_course_form.data['programming_language']
            id_course = str(year_course) + str(period_course) + str(code_course) + str(group_course)
            id_academic_period = year_course + period_course

            data = {
                "id_course": id_course,
                "code_course": code_course,
                "name_course": name_course,
                "credits_course": credits_course,
                "professor_course": professor_course,
                "group_course": group_course,
                "programming_language": programming_language,
                "period_course": period_course,
                "year_course": year_course,
                "academic_period": id_academic_period
            }

            #Checking if course is not exist
            response_1=(check_course(id_course)).decode('utf-8')

            if response_1 == '404':

                serializer = CourseSerializer(data=data)

                if serializer.is_valid():
                    # checking if academic period is not exist
                    response_2 = (check_period(data['academic_period'])).decode('utf-8')

                    if response_2 == '404':
                        name_academic_period = ""
                        if data['period_course'] == '01':
                            name_academic_period = 'February - June / ' + data['year_course']
                        if data['period_course'] == '02':
                            name_academic_period = 'August - December / ' + data['year_course']

                        data_period = {
                            "id_academic_period": data['academic_period'],
                            "name_academic_period": name_academic_period
                        }
                        data_period_str = json.dumps(data_period)
                        data_period_enc = data_period_str.encode('utf-8')


                        # -------creating period -------->
                        create_period(data_period_enc)

                    # -------creating course -------->

                    data_str = json.dumps(data)
                    print("data str")
                    print(data_str)
                    data_enc = data_str.encode('utf-8')
                    print("data enc")
                    print(data_enc )

                    response_3 = create_course(data_enc)
                    print("respuesta de crear curso")
                    print(response_3.decode('utf-8'))


                    if response_3.decode('utf-8') == '201':

                        # -------running container -------->
                        id_image = programming_language.encode('utf-8')
                        image_data = json.loads((get_image_detail(id_image)).decode('utf-8'))

                        image = image_data['name_image']
                        name_vol_container = id_course + "_backup_db"

                        data_container = {
                            "id_course": id_course,
                            "image": image,
                            "name_vol_container": name_vol_container,
                        }

                        data_container_str = json.dumps(data_container)
                        data_container_enc = data_container_str.encode('utf-8')

                        response_4 = run_container(data_container_enc)

                        print("response 4")
                        print(type(response_4))
                        print(response_4)


                        if response_4.decode('utf-8') == '0':
                            print("contenedor corriendo")


                            print("id curso")
                            print(id_course)
                            data_container = get_data_container(id_course)
                            print("datos contenedor")
                            print(type(data_container))
                            print(data_container)
                            response_5 = create_container(data_container)
                            print("container registrado")
                            print(type(response_5))
                            print(response_5)

                            if response_5.decode('utf-8') == '201':

                                # modificar contrasena de admin
                                print("id del curso")
                                print(id_course)
                                print("id profesor")
                                print(id_professor)


                                data_set_pass = {
                                    "id_professor" : id_professor,
                                    "name_professor": str(user.first_name),
                                    "lastname_professor": str(user.last_name),
                                    "email_professor" : str(user.email),
                                    "id_course" : id_course,
                                }
                                print("datos profe")
                                print(data_set_pass)

                                data_set_pass_str = json.dumps(data_set_pass)
                                print("data_set_pass_str")
                                print(data_set_pass_str)
                                print(type(data_set_pass_str))

                                data_set_pass_enc = data_set_pass_str.encode('utf-8')
                                print("data_set_pass_enc")
                                print(data_set_pass_enc)
                                print(type(data_set_pass_enc))

                                response_6 = set_pass_professor(data_set_pass_enc)
                                print("response_6")
                                print("el lazo 1")
                                print(response_6)

                                if response_6.decode('utf-8') == '201':

                                    return redirect("created_course/")
                                else:
                                    return redirect("fail_course/")

                else:
                    print(serializer.errors)


            if response_1 == '200':
                messages.error(request, "This course already exists")




        elif config_profile_form.is_valid():
            print("es formulario de configuracion")


    return render(request, "profile/professor_profile.html", context)
    #return HttpResponseRedirect("/profile/professor_profile.html", context)

def page_created_course(request):
    return render(request, "profile/created_course.html")

def page_fail_course(request):
    return render(request, "profile/fail_course.html")





def download_db_domjudge(request,id_course):
    path='/var/lib/docker/volumes/'+id_course+'_backup_db/_data/'
    os.system('cd '+path+' && tar czf domjudge.tar.gz domjudge')
    filepath = '/var/lib/docker/volumes/'+id_course+'_backup_db/_data/domjudge.tar.gz'
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))








