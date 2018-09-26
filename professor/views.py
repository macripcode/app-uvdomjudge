import os
import json
import time
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.static import serve
from .forms import CreateCourseForm
from .forms import RubricForm
from .models import Rubric, Evaluation
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
from request.clients import client_professor_get_data_contest_container
import xlsxwriter as xlsw



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



    context={
        'courses_professor': courses_professor,
        'create_course_form': create_course_form,
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
    if request.method == 'GET' and request.is_ajax():
        print ("cositas")

    data_str = client_professor_get_data_contest_container(id_course).decode('utf-8')
    context = json.loads(data_str)
    generate_file_rubric_and_evaluation_for_contest(context, id_course)
    course_enc = client_public_get_course(id_course)
    course_str = ((course_enc).decode('utf-8')).replace('Ã³','ó')
    course = json.loads(course_str)
    course['professor_name'] = get_professor(course['professor_course'])
    context["course"] = course
    rubric_form = RubricForm()
    rubric_form.fields['terminal_objetive'].widget.attrs = {
        'id': 'id_textarea_term_obj_'+id_course,
        'class': 'materialize-textarea',
    }
    rubric_form.fields['activity'].widget.attrs = {
        'id': 'id_textarea_activity_' + id_course,
        'class': 'materialize-textarea',
    }
    context['rubric_form'] = rubric_form
    print(context)


    return render(request, "profile/course_profile.html", context)


def check_rubric(request, id_course):
    if request.method == 'GET'  and request.is_ajax():
        data = {}
        problem_id = request.GET['problem_id']

        try:
            rubric = Rubric.objects.get(problem_id=problem_id)
            data['exists'] = "true"
            data['terminal_objetive'] = rubric.terminal_objetive
            data['activity'] = rubric.activity
            data['approved'] = rubric.approved
            data['notapproved'] = rubric.notapproved
            data['weight'] = rubric.weight

        except Rubric.DoesNotExist:
            data['exists'] = "false"

    return JsonResponse(data)

def save_rubric(request, id_course):
    if request.method == 'GET'  and request.is_ajax():
        message = ""
        id_contest = request.GET['id_contest']
        id_problem = request.GET['id_problem']
        terminal_objetive =  request.GET['terminal_objetive']
        activity =  request.GET['activity']
        weight =  request.GET['weight']
        approved = request.GET['approved']
        notapproved = request.GET['notapproved']

        try:
            rubric = Rubric.objects.get(problem_id=id_problem)
            rubric.course_id = id_course
            rubric.contest_id = id_contest
            rubric.problem_id = id_problem
            rubric.terminal_objetive = terminal_objetive
            rubric.activity = activity
            rubric.approved = approved
            rubric.notapproved = notapproved
            rubric.weight = weight
            rubric.save()
            message += "Rubric has been saved"

        except Rubric.DoesNotExist:

            rubric = Rubric(
                course_id=id_course,
                terminal_objetive=terminal_objetive,
                activity=activity,
                weight=weight,
                approved=approved,
                notapproved=notapproved,
                problem_id=id_problem,
                contest_id=id_contest

            )
            rubric.save()
            message += "Rubric has been saved."

    else:
        message += "Rubric has not been saved"

    return JsonResponse({'message': message})

def generate_file_rubric_and_evaluation_for_contest(context, id_course):

    #------- Generating Rubric File------->

    for contest in context['contests']:
        workbook = xlsw.Workbook('static/rubric_contest_'+str(contest[0])+'.xlsx')
        worksheet = workbook.add_worksheet()
        current_row = 0
        for problem in contest[3]:
            #--formats cell -->
            format_problem_title = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            normal = workbook.add_format({
                'border': 1,
                'text_wrap': 1,
                'valign':'vcenter'
            })
            #normal.set_align('vjustify')
            bold =  workbook.add_format({
                'border': 1,
                'bold': 1,
                'align': 'center',
                'valign': 'vcenter'
            })

            center = workbook.add_format({
                'align': 'center',
                'border': 1,
                'valign':'vcenter'
            })
            # --formats cell --->
            # -- Adding cells -->

            worksheet.set_row(current_row, 30)
            worksheet.set_column('A:E', 20)
            worksheet.write(current_row, 0, "Problem:" , format_problem_title)
            worksheet.merge_range(current_row,1,current_row,4, problem[1], format_problem_title)

            current_row+=1

            worksheet.set_row(current_row, 30)
            worksheet.write(current_row, 0, "Terminal Objetive",bold)
            worksheet.write(current_row, 1, "Activity",bold)
            worksheet.write(current_row, 2, "Weigth",bold)
            worksheet.write(current_row, 3, "Level 4: 5.0",bold)
            worksheet.write(current_row, 4, "Level 1: 0.0",bold)

            current_row += 1

            #--Get rubric for each problem---->
            try:
                rubric = Rubric.objects.get(problem_id=problem[0])
                worksheet.set_row(current_row, 100)
                worksheet.write(current_row, 0, rubric.terminal_objetive,normal)
                worksheet.write(current_row, 1, rubric.activity, normal)
                worksheet.write(current_row, 2, rubric.weight, center)
                worksheet.write(current_row, 3, rubric.approved, normal)
                worksheet.write(current_row, 4, rubric.notapproved, normal)

            except Rubric.DoesNotExist:
                print ("rubric does not exist.")
            # --Get rubric for each problem---->

            current_row += 3
            # -- Adding cells -->

        workbook.close()
        # ------- Generating Rubric File------->

        # ------- Generating Evaluation File------->
        workbook = xlsw.Workbook('static/evaluation_contest_' + str(contest[0]) + '.xlsx')
        worksheet = workbook.add_worksheet()

        # --formats cell -->
        format_problem_title = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        normal = workbook.add_format({
            'border': 1,
            'text_wrap': 1,
            'valign': 'vcenter'
        })

        bold = workbook.add_format({
            'border': 1,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        center = workbook.add_format({
            'align': 'center',
            'border': 1,
            'valign': 'vcenter'
        })
        # --formats cell --->

        #--------- Header ---------->
        worksheet.set_row(0, 100)
        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 40)
        worksheet.merge_range(0, 0, 0, 1 ,"Terminal Objetive", bold)
        worksheet.set_row(1,100)
        worksheet.merge_range(1, 0, 1, 1, "Activity", bold)
        worksheet.set_row(2, 20)
        worksheet.merge_range(2, 0, 2, 1, "Weight", bold)
        worksheet.set_row(3, 20)
        worksheet.write(3, 0, "Code", bold)
        worksheet.write(3, 1, "Name", bold)
        # --------- Header ---------->

        # ----------Writing list students----------------------->

        current_column_evaluation = 0
        current_row_evaluation = 4

        for student in context['list']:
            worksheet.write(current_row_evaluation, current_column_evaluation, student[0], normal)
            current_column_evaluation += 1
            worksheet.write(current_row_evaluation, current_column_evaluation, student[1], normal)
            current_column_evaluation = 0
            current_row_evaluation += 1
        # ----------Writing list students----------------------->

        #----------Writing Terminal objective, Activity and weight for each problem--->
        current_column_evaluation = 2
        current_row_evaluation = 0

        for problem in contest[3]:

            try:
                #--------Adding rubric to the file ----------------->
                rubric = Rubric.objects.get(problem_id=problem[0])
                worksheet.set_column(current_column_evaluation, current_column_evaluation, 30)
                worksheet.write(current_row_evaluation, current_column_evaluation, rubric.terminal_objetive, normal)
                current_row_evaluation += 1
                worksheet.write(current_row_evaluation, current_column_evaluation, rubric.activity, normal)
                current_row_evaluation += 1
                worksheet.write(current_row_evaluation, current_column_evaluation, rubric.weight, normal)

                # --------Adding rubric to the file ----------------->

                # ----------Writing evaluation for each student by problem----------------------->
                current_row_evaluation = 4
                for e in context['evaluation']:
                    if e[0]== contest[0] and e[1] == problem[0]:
                        for evaluations_student in e[2]:

                            worksheet.write_number(current_row_evaluation, current_column_evaluation, (evaluations_student*(int(rubric.weight)/100)))
                            current_row_evaluation += 1
                # ----------Writing evaluation for each student by problem---------------------->

                current_column_evaluation +=1
                current_row_evaluation = 0



            except Rubric.DoesNotExist:
                print ("rubric does not exist.")
            # --Get rubric for each problem---->

        from xlsxwriter.utility import xl_rowcol_to_cell
        from xlsxwriter.utility import xl_range


        current_row_evaluation = 4

        worksheet.write((current_row_evaluation-1), current_column_evaluation, "Total", bold)

        for student in context['list']:
            range_sum = xl_range(current_row_evaluation, 2, current_row_evaluation, (current_column_evaluation-1))
            cell_to_write = xl_rowcol_to_cell(current_row_evaluation, current_column_evaluation)
            worksheet.write_formula(cell_to_write, '{=SUM('+range_sum+')}')
            current_row_evaluation += 1

        workbook.close()
    # ------- Generating Evaluation File------->

    return 0









