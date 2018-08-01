import os
import json
import time
from django.contrib import messages
from django.http import JsonResponse
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
from request.clients import client_professor_get_data_container
from request.clients import create_container
from request.clients import client_professor_exist_course
from request.clients import client_professor_filter_by_professor_course
from request.clients import client_public_get_container
from request.clients import client_public_exist_container
from request.clients import client_public_run_container
from request.clients import set_pass_professor
from request.clients import client_professor_get_port_80_container
from request.clients import client_professor_get_port_3306_container
from request.clients import client_professor_start_container
from request.clients import client_professor_stop_container
from request.clients import client_professor_remove_container
from request.clients import client_professor_show__logs_container
from request.clients import client_professor_put_container
from request.clients import client_professor_delete_course
from request.clients import client_public_run_container
from request.clients import client_professor_open_database_container
from request.clients import client_public_get_course
from request.utils import get_professor



def professor_profile(request):
    # ------- get courses by professor ------------>
    user = request.user
    id_professor = str(user.id)
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
            if response_1_enc.decode('utf-8') == '200':
                response_2_enc = client_public_run_container(course['id_course'])
                if response_2_enc.decode('utf-8') == 'true':
                    course['status']='true'
                    port_80_container = client_professor_get_port_80_container(course['id_course']).decode('utf-8')
                    course['url_judge'] = 'http://localhost:' + port_80_container + '/domjudge/public/login.php'
                    course['url_page'] = course['id_course'] + '/course'
                if response_2_enc.decode('utf-8') == 'false':
                    course['status'] = 'false'
                    course['url_judge'] = 'The container is not running. The virtual judge can not be accessed.'
                    course['url_page'] = 'The container is not running. The course page can not be accessed.'

                courses_professor.append(course)
        if len(courses_professor) == 0:
            messages.error(request, "There's no courses currently.")


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
            response_1 = (client_professor_exist_course(id_course)).decode('utf-8')
            print("Verifing if course exist...")
            print("response_1")
            print(response_1)

            if response_1 == '404':
                serializer = CourseSerializer(data=data)
                if serializer.is_valid():
                    # checking if academic period is not exist
                    response_2 = (client_professor_exist_period(data['academic_period'])).decode('utf-8')
                    print("Checking period...")
                    print("response_2")
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
                    data_enc = data_str.encode('utf-8')
                    response_3 = (client_professor_create_course(data_enc)).decode('utf-8')
                    print("Creating course on api...")
                    print("response_3")
                    print(response_3)

                    if response_3 == '201':
                        # -------creating container -------->
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
                        response_4 = (client_professor_run_container(data_container_enc)).decode('utf-8')
                        time.sleep(8)
                        print("Creating container and executing...")
                        print("response_4")
                        print(response_4)
                        #------ the container has been created------->
                        if response_4 == '200':
                            response_5_enc = client_public_run_container(id_course)
                            response_5 = response_5_enc.decode('utf-8')
                            print("Verifing if container is running...")
                            print("response_5")
                            print(response_5)

                            if response_5 == 'true':
                                response_6 = (client_professor_open_database_container(id_course)).decode('utf-8')
                                time.sleep(4)
                                print("Registe user in database...")
                                print("response_6")
                                print(response_6)

                                #-------check if container is running------->
                                data_container = client_professor_get_data_container(id_course)
                                response_7 = create_container(data_container)
                                print("Register container into api...")
                                print("response_7")
                                print(response_7)

                                if response_7.decode('utf-8') == '201':
                                    data_set_pass = {
                                        "id_professor" : id_professor,
                                        "name_professor": str(user.first_name),
                                        "lastname_professor": str(user.last_name),
                                        "email_professor" : str(user.email),
                                        "id_course" : id_course,
                                    }

                                    data_set_pass_str = json.dumps(data_set_pass)
                                    data_set_pass_enc = data_set_pass_str.encode('utf-8')
                                    response_8 = (set_pass_professor(data_set_pass_enc)).decode('utf-8')
                                    print("Creating user asociated to professor in database...")
                                    print("response_8")
                                    print(response_8)

                                    if response_8 == '201':
                                        return redirect("created_course/")
                                    else:
                                        return redirect("fail_course/")
                                else:
                                    messages.error(request, "The container associated to the course could not be registered on Api.")
                            else:
                                messages.error(request, "The container associated to the course is not in execution.")
                        else:
                            messages.error(request, "The container associated to the course could not be executed.")
                    else:
                        messages.error(request, "This course could not be created.")

                else:
                    print(serializer.errors)


            if response_1 == '200':
                messages.error(request, "This course already exists.")


    return render(request, "profile/professor_profile.html", context)


def page_created_course(request):
    return render(request, "profile/created_course.html")

def page_fail_course(request):
    return render(request, "profile/fail_course.html")

def download_db_domjudge(request,id_course):
    path='/var/lib/docker/volumes/'+id_course+'_backup_db/_data/'
    os.system('cd '+path+' && tar czf domjudge.tar.gz domjudge')
    filepath = '/var/lib/docker/volumes/'+id_course+'_backup_db/_data/domjudge.tar.gz'
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def play_container(request):
    #have to be stopped
    if request.method == 'GET'  and request.is_ajax():
        message = ""
        id_course = request.GET['id_course']
        response = client_professor_start_container(id_course).decode('utf-8')
        port_80 = client_professor_get_port_80_container(id_course).decode('utf-8')
        port_3306 = client_professor_get_port_3306_container(id_course).decode('utf-8')
        response2 = update_container_api(id_course,port_80,port_3306)
        if response == '200' and response2 == '200':
            message = 'the container '+ id_course+' has been resumed and api has been update.'
        else:
            message = 'the container ' + id_course + ' has not been resumed'
    return JsonResponse({'message': message})

def stop_container(request):
    #have to be runing

    if request.method == 'GET'  and request.is_ajax():
        message = ""
        id_course = request.GET['id_course']
        response = client_professor_stop_container(id_course).decode('utf-8')
        response2 = update_container_api(id_course, "none", "none")
        if response == '200' and response2=='200':
            message = 'the container '+ id_course+' has been stopped and api has been update.'
        else:
            message = 'the container ' + id_course + ' has not been stopped'
    return JsonResponse({'message': message})

def remove_container(request):
    if request.method == 'GET'  and request.is_ajax():
        message = ""
        id_course = request.GET['id_course']
        response = client_public_run_container(id_course).decode('utf-8')
        #if container is running then stop it
        if response == 'true':
            client_professor_stop_container(id_course).decode('utf-8')

        response1 = client_professor_remove_container(id_course).decode('utf-8')
        if response1 == '200':

            response2 = client_professor_delete_course(id_course).decode('utf-8')
            if response2 == '200':
                message = 'the container '+ id_course+' has been removed and api has been update.'
        else:
            message = 'the container ' + id_course + ' has not been removed'

    return JsonResponse({'message': message})

def logs_container(request):
    if request.method == 'GET'  and request.is_ajax():
        id_course = request.GET['id_course']
        message = "<---- Logs of Container "+id_course+" ---->\n\n"
        response = client_professor_show__logs_container(id_course).decode('utf-8')
        message += response

    return JsonResponse({'message': message})

#Update port 80 and 3306 in container's api
def update_container_api(name_container, new_port_80, new_port_3306):
    container_enc = client_public_get_container(name_container)
    container_str = container_enc.decode('utf-8')
    container = json.loads(container_str)
    container['port_number_80_container'] = new_port_80
    container['port_number_3306_container'] = new_port_3306
    container2_str = json.dumps(container)
    container2_enc= container2_str.encode('utf-8')
    response2 = client_professor_put_container(container2_enc)
    if response2.decode('utf-8') == '200':
        return '200'
    return '500'

def course_profile(request, id_course):
    print(id_course)
    context = {}
    course_enc = client_public_get_course(id_course)
    course_str = ((course_enc).decode('utf-8')).replace('Ã³','ó')
    course = json.loads(course_str)
    course['professor_name'] = get_professor(course['professor_course'])

    context["course"] = course

    return render(request, "profile/course_profile.html", context)









