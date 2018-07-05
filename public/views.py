import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import RegistrationForm
from request.clients import client_public_get_courses
from request.clients import get_course_detail
from request.clients import client_public_get_container
from request.clients import enroll_student
from request.clients import client_public_exist_container
from request.clients import client_public_run_container
from request.clients import get_user_detail


def public_page(request):

    courses_in_api = json.loads((client_public_get_courses()).decode('utf-8'))
    current_courses = []

    if len(courses_in_api) == 0:
        messages.error(request, "There are no courses currently")

    if len(courses_in_api) > 0 :

        for i in range(0, len(courses_in_api)):

            course = courses_in_api[i]
            response_1_enc= client_public_exist_container(course['id_course'])
            response_1 = response_1_enc.decode('utf-8')
            if response_1 == '200':
                response_2_enc = client_public_run_container(course['id_course'])
                response_2 = response_2_enc.decode('utf-8')
                if response_2 == 'true':
                    course['professor_name'] = get_professor(course['professor_course'])
                    id_course = course['id_course']
                    container_enc = client_public_get_container(id_course)
                    container_str = container_enc.decode('utf-8')
                    container = json.loads(container_str)
                    port_80_container = container['port_number_80_container']
                    url = 'http://localhost:' + port_80_container + '/domjudge/public/login.php'
                    course['url'] = url
                    current_courses.append(course)

        if len(current_courses) == 0:
            messages.error(request, "There's no courses currently.")

        context={
            "current_courses": current_courses,
        }
    return render(request, "public/get_courses.html", context)


def enroll_course(request, id_course):

    course_enc = get_course_detail(id_course)
    course_str = ((course_enc).decode('utf-8')).replace('Ã³','ó')
    course = json.loads(course_str )
    course['professor_name'] = get_professor(course['professor_course'])
    registration_form = RegistrationForm()
    context = {
        "course": course,
        "registration_form": registration_form,
    }

    # ------- getting container with id_course ------------>

    container_bites=client_public_get_container(id_course)
    container_str=container_bites.decode('utf-8')
    container=json.loads(container_str)

    # ------- getting port 3306 from container  ------------>
    port_number_3306_container=container['port_number_3306_container']

    # ------- register student on course  ------------>
    if request.method == 'POST':

        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            code_student = request.POST['code_student']
            name_student = request.POST['name_student']
            lastname_student = request.POST['lastname_student']
            email_student = request.POST['email_student']

            data = {
                "name_container": id_course,
                "port_number_3306_container":port_number_3306_container,
                "code_student" : code_student,
                "name_student" : name_student,
                "lastname_student" : lastname_student,
                "email_student" : email_student,
            }

            data_enc=(json.dumps(data)).encode('utf-8')
            response_1=enroll_student(data_enc)

            print(response_1)

            if response_1.decode('utf-8') == '201':
                messages.success(request, "You have been successfully registered.")
            else:
                messages.error(request, "You could not be registered.")


    return render(request, "public/enroll_course.html", context)


#This function get all the professor from db
def get_professor(id_professor):

    professor=User.objects.get(id=id_professor);    
    return str(professor.first_name)+" "+str(professor.last_name)
    

    

