from .client_public_get_courses import ClientPublicGetCourses
from .client_public_get_course import ClientPublicGetCourse
from .client_professor_create_course import ClientProfessorCreateCourse
from .client_professor_run_container import ClientProfessorRunContainer
from .client_professor_get_image import ClientProfessorGetImage
from .client_enroll_public import EnrollStudentPublic
from .client_public_get_container import ClientPublicGetContainer
from .client_professor_exist_period import ClientProfessorExistPeriod
from .client_professor_create_period import ClientProfessorCreatePeriod
from .client_professor_get_data_container import ClientProfessorGetDataContainer
from .client_create_container_professor import CreateContainerProfessor
from .client_professor_exist_course import ClientProfessorExistCourse
from .client_professor_filter_by_professor_courses import ClientProfessorFilterByProfessorCourse
from .client_set_pass_professor import SetPassProfessorClient
from .client_periods_administrator import PeriodsAdministratorClient
from .client_delete_courses_period_administrator import DeletePeriodCoursesAdministratorClient
from .client_delete_containers_period_administrator import DeletePeriodContainersAdministratorClient
from .client_delete_period_administrator import DeletePeriodAdministratorClient
from .client_create_user_administrator import CreateUserAdministratorClient
from .client_public_user_detail import ClientPublicUserDetail
from .client_public_exists_container import ClientPublicExistContainer
from .client_public_run_container import ClientPublicRunContainer
from .client_professor_get_port_80_container import ClientProfessorGetPort80Container
from .client_professor_get_port_3306_container import ClientProfessorGetPort3306Container
from .client_professor_stop_container import ClientProfessorStopContainer
from .client_professor_start_container import ClientProfessorStartContainer
from .client_professor_remove_container import ClientProfessorRemoveContainer
from .client_professor_show_logs_container import ClientProfessorShowLogsContainer
from .client_professor_put_container import ClientProfessorPutContainer
from .client_professor_open_database_container import ClientProfessorOpenDataBaseContainer
from .client_professor_delete_course import ClientProfessorDeleteCourse


#delete course and associated container from the api
def client_professor_delete_course(id_course):
    request = ClientProfessorDeleteCourse()
    response = request.call(id_course)
    return response

# Check if the course already exist
def client_professor_exist_course(id_course):
    request= ClientProfessorExistCourse()
    response = request.call(id_course)
    return response

# modify a existe container in the api
def client_professor_put_container(container):
    request = ClientProfessorPutContainer()
    response = request.call(container)
    return response

# Check if the period already exist
def client_professor_exist_period(id_period):
    request= ClientProfessorExistPeriod()
    response = request.call(id_period)
    return response

#check the current port 80 of name_container
def client_professor_get_port_80_container(name_container):
    request = ClientProfessorGetPort80Container()
    response = request.call(name_container)
    return response

#check the current port 3306 of name_container
def client_professor_get_port_3306_container(name_container):
    request = ClientProfessorGetPort3306Container()
    response = request.call(name_container)
    return response

#stop a container
def client_professor_stop_container(name_container):
    request = ClientProfessorStopContainer()
    response = request.call(name_container)
    return response

#start a container
def client_professor_start_container(name_container):
    request = ClientProfessorStartContainer()
    response = request.call(name_container)
    return response

#remove a container
def client_professor_remove_container(name_container):
    request = ClientProfessorRemoveContainer()
    response = request.call(name_container)
    return response

#show logs from a runing container
def client_professor_show__logs_container(name_container):
    request = ClientProfessorShowLogsContainer()
    response = request.call(name_container)
    return response

#make de database more flexible to insert an get querys in a running container
def client_professor_open_database_container(name_container):
    request = ClientProfessorOpenDataBaseContainer()
    response = request.call(name_container)
    return response

#--------professor client-------->

def client_public_exist_container(name_container):
    #check if container exist in the api's db
    request = ClientPublicExistContainer()
    response = request.call(name_container)
    return response

def client_public_run_container(name_container):
    #check if container with name_container is running currently
    request = ClientPublicRunContainer()
    response = request.call(name_container)
    return response


def client_public_get_container(name_container):
    #get the info of container from api's db
    request = ClientPublicGetContainer()
    response = request.call(name_container)
    return response


def client_public_get_course(id_course):
    course_request = ClientPublicGetCourse()
    response = course_request.call(id_course)
    return response

def get_user_detail(id_user):
    user_request = ClientPublicUserDetail()
    response = user_request.call(id_user)
    return response


def client_public_get_courses():
    courses_request = ClientPublicGetCourses()
    response = courses_request.call()
    return response


# Register on api the container's data
def create_container(container):
    request = CreateContainerProfessor()
    response = request.call(container)
    return response


def client_professor_create_course(course):
    course_request = ClientProfessorCreateCourse()
    response = course_request.call(course)
    return response


def client_professor_create_period(period):
    request=ClientProfessorCreatePeriod()
    response = request.call(period)
    return response


def create_user(user):
    print("llego 1")
    request = CreateUserAdministratorClient()
    response = request.call(user)
    return response


# This function get data of container that is not yet register on api
def client_professor_get_data_container(name_container):
    request = ClientProfessorGetDataContainer()
    response = request.call(name_container)
    return response


def enroll_student(data):
    request = EnrollStudentPublic()
    response=request.call(data)
    return response


def client_professor_get_image(id_image):
    request = ClientProfessorGetImage()
    response = request.call(id_image)
    return response


def client_professor_run_container(container):
    request = ClientProfessorRunContainer()
    response = request.call(container)
    return response


def client_professor_filter_by_professor_course(id_professor):
    request = ClientProfessorFilterByProfessorCourse()
    response = request.call(id_professor)
    return response


def set_pass_professor(data):
    request = SetPassProfessorClient()
    print("el lazo 2")
    response = request.call(data)
    return response

def get_periods():
    periods_request = PeriodsAdministratorClient()
    response = periods_request.call()
    return response


def delete_period_courses(id_period):
    request = DeletePeriodCoursesAdministratorClient()
    response = request.call(id_period)
    return response


def delete_period_containers(id_period):
    request = DeletePeriodContainersAdministratorClient()
    response = request.call(id_period)
    return response

def delete_period(id_period):
    request = DeletePeriodAdministratorClient()
    response = request.call(id_period)
    return response



