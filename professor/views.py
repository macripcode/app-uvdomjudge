import os
import json
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.static import serve
from .forms import CreateCourseForm
from .forms import ConfigProfileForm
from request.serializers import CourseSerializer
from request.clients import client_professor_create_course
from request.clients import client_professor_get_image
from request.clients import client_professor_run_container
from request.clients import client_professor_exist_period
from request.clients import client_professor_create_period
from request.clients import get_data_container
from request.clients import create_container
from request.clients import client_professor_exist_course
from request.clients import client_professor_filter_by_professor_course
from request.clients import client_public_get_container
from request.clients import client_public_exist_container
from request.clients import client_public_run_container
from request.clients import set_pass_professor


def professor_profile(request):
    # ------- get courses by professor ------------>
    user = request.user
    id_professor = str(user.id)
    #---send token too and validate
    print(id_professor)
    courses_professor_in_api_enc = client_professor_filter_by_professor_course(id_professor)
    courses_professor_in_api_str = (courses_professor_in_api_enc.decode('utf-8')).replace('Ã³','ó')
    courses_professor_in_api = json.loads(courses_professor_in_api_str)
    courses_professor = []
    # ------- assigning url to each course ------------>

    if len(courses_professor_in_api) == 0:
        messages.error(request, "There are no courses currently")

    if len(courses_professor_in_api) > 0 :

        for i in range(0, len(courses_professor_in_api)):
            course = courses_professor_in_api[i]
            response_1_enc = client_public_exist_container(course['id_course'])
            response_1 = response_1_enc.decode('utf-8')
            if response_1 == '200':
                id_course = course['id_course']
                container_enc=client_public_get_container(id_course)
                print("pidio el contenedor")
                container_str=container_enc.decode('utf-8')
                print(container_str)
                container=json.loads(container_str)
                port_80_container=container['port_number_80_container']
                url='http://localhost:'+port_80_container+'/domjudge/public/login.php'
                course['url']=url
                courses_professor.append(course)

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

    if request.method == 'POST':
        create_course_form = CreateCourseForm(request.POST)

        if create_course_form.is_valid():
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
            response_1=(client_professor_exist_course(id_course)).decode('utf-8')

            if response_1 == '404':
                serializer = CourseSerializer(data=data)
                if serializer.is_valid():
                    # checking if academic period is not exist
                    response_2 = (client_professor_exist_period(data['academic_period'])).decode('utf-8')
                    print("Checking period")
                    print(response_2)

                    if response_2 == '404':
                        #-----creating a period on api if it not exists---------->
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
                        client_professor_create_period(data_period_enc)

                    # -------creating course on api-------->

                    data_str = json.dumps(data)
                    print("data str")
                    print(data_str)
                    data_enc = data_str.encode('utf-8')
                    print("data enc")
                    print(data_enc )

                    response_3 = client_professor_create_course(data_enc)
                    print("respuesta de crear curso")
                    print(response_3.decode('utf-8'))


                    if response_3.decode('utf-8') == '201':
                        # -------running container -------->
                        id_image = programming_language.encode('utf-8')
                        image_data = json.loads((client_professor_get_image(id_image)).decode('utf-8'))

                        image = image_data['name_image']
                        name_vol_container = id_course + "_backup_db"

                        data_container = {
                            "id_course": id_course,
                            "image": image,
                            "name_vol_container": name_vol_container,
                        }

                        data_container_str = json.dumps(data_container)
                        data_container_enc = data_container_str.encode('utf-8')
                        response_4 = client_professor_run_container(data_container_enc)
                        print("response 4")
                        print(type(response_4))
                        print(response_4)
                        #------ the container has been created------->
                        if response_4.decode('utf-8') == '0':
                            response_5_enc = client_public_run_container(id_course)
                            response_5 = response_5_enc.decode('utf-8')
                            print("container is running?")
                            print(response_5)

                            if response_5 == 'true':
                                # ------ the container is up------->
                                #tarea colocar la misma funcion en el view de public
                                print("contenedor corriendo")
                                # print("id curso")
                                # print(id_course)
                                # #-------check if container is running------->
                                # data_container = get_data_container(id_course)
                                # print("datos contenedor")
                                # print(type(data_container))
                                # print(data_container)
                                # response_6 = create_container(data_container)
                                # print("container registrado")
                                # print(type(response_6))
                                # print(response_6)

                                # if response_6.decode('utf-8') == '201':
                                #
                                #     # modificar contrasena de admin
                                #     print("id del curso")
                                #     print(id_course)
                                #     print("id profesor")
                                #     print(id_professor)
                                #
                                #
                                #     data_set_pass = {
                                #         "id_professor" : id_professor,
                                #         "name_professor": str(user.first_name),
                                #         "lastname_professor": str(user.last_name),
                                #         "email_professor" : str(user.email),
                                #         "id_course" : id_course,
                                #     }
                                #     print("datos profe")
                                #     print(data_set_pass)
                                #
                                #     data_set_pass_str = json.dumps(data_set_pass)
                                #     print("data_set_pass_str")
                                #     print(data_set_pass_str)
                                #     print(type(data_set_pass_str))
                                #
                                #     data_set_pass_enc = data_set_pass_str.encode('utf-8')
                                #     print("data_set_pass_enc")
                                #     print(data_set_pass_enc)
                                #     print(type(data_set_pass_enc))
                                #
                                #     response_7 = set_pass_professor(data_set_pass_enc)
                                #     print("response_7")
                                #     print("el lazo 1")
                                #     print(response_7)
                                #
                                #     if response_7.decode('utf-8') == '201':
                                #
                                #         return redirect("created_course/")
                                #     else:
                                #         return redirect("fail_course/")

                            else:
                                messages.error(request, "The container associated to the course is not in execution.")





                        else:
                            messages.error(request, "The container associated to the course could not be executed.")
                    else:
                        messages.error(request, "This course can not be created.")

                else:
                    print(serializer.errors)


            if response_1 == '200':
                messages.error(request, "This course already exists.")




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








