from django.shortcuts import render
from .forms import RegistrationForm
from request.clients import get_courses
from request.clients import get_course_detail
from request.clients import get_container
from request.clients import enroll_student
from django.contrib import messages

from django.contrib.auth.models import User
import json


# Create your views here.


def public_page(request):

    current_courses = json.loads((get_courses()).decode('utf-8'))


    """
     # ------- assigning url to each course ------------>

    for course in courses_professor:
        id_course=course['id_course']
        container_enc=get_container(id_course)
        container_str=container_enc.decode('utf-8')
        container=json.loads(container_str)
        port_80_container=container['port_number_80_container']
        url='http://localhost:'+port_80_container+'/domjudge/public/login.php'
        course['url']=url
    
    """
    for course in current_courses:

        course['professor_name']=get_professor(course['professor_course'])
        id_course = course['id_course']
        container_enc = get_container(id_course)
        container_str = container_enc.decode('utf-8')
        container = json.loads(container_str)
        port_80_container = container['port_number_80_container']
        url = 'http://localhost:' + port_80_container + '/domjudge/public/login.php'
        course['url'] = url

    print(current_courses)
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

    container_bites=get_container(id_course)
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
    

    

