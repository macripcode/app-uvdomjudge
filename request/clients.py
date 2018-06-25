from .client_courses_public import CoursesPublicClient
from .client_course_public import CoursePublicClient
from .client_create_course_professor import CreateCourseProfessor
from .client_run_container_professor import RunContainerProfessor
from .client_image import ImageProfessorClient
from .client_enroll_public import EnrollStudentPublic
from .client_container_public import ContainerPublicClient
from .client_check_period_professor import CheckPeriodProfessorClient
from .client_create_period_professor import PeriodCreateProfessorClient
from .client_data_container_professor import ContainerDataProfessorClient
from .client_create_container_professor import CreateContainerProfessor
from .client_check_course_professor import CheckCourseProfessorClient
from .client_courses_by_professor import CoursesByProfessorClient
from .client_set_pass_professor import SetPassProfessorClient
from .client_periods_administrator import PeriodsAdministratorClient
from .client_delete_courses_period_administrator import DeletePeriodCoursesAdministratorClient
from .client_delete_containers_period_administrator import DeletePeriodContainersAdministratorClient
from .client_delete_period_administrator import DeletePeriodAdministratorClient



# Check if the course already exist
def check_course(id_course):
    request= CheckCourseProfessorClient()
    response = request.call(id_course)
    return response


def check_period(id_period):
    request= CheckPeriodProfessorClient()
    response = request.call(id_period)
    return response


def get_container(name_container):
    request = ContainerPublicClient()
    response = request.call(name_container)
    return response


def get_course_detail(id_course):
    course_request = CoursePublicClient()
    response = course_request.call(id_course)
    return response


def get_courses():
    courses_request = CoursesPublicClient()
    response = courses_request.call()
    return response


# Register on api the container's data
def create_container(container):
    request = CreateContainerProfessor()
    response = request.call(container)
    return response


def create_course(course):
    course_request=CreateCourseProfessor()
    response = course_request.call(course)
    return response


def create_period(period):
    request=PeriodCreateProfessorClient()
    response = request.call(period)
    return response


# This function get data of container that is not yet register on api
def get_data_container(name_container):
    request = ContainerDataProfessorClient()
    response = request.call(name_container)
    return response


def enroll_student(data):
    request = EnrollStudentPublic()
    response=request.call(data)
    return response


def get_image_detail(id_image):
    request = ImageProfessorClient()
    response = request.call(id_image)
    return response


def run_container(container):
    request = RunContainerProfessor()
    response = request.call(container)
    return response


def get_courses_by_professor(id_professor):
    request = CoursesByProfessorClient()
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

