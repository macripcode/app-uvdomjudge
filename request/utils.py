from django.contrib.auth.models import User

#This function get all the professor from db
def get_professor(id_professor):

    professor = User.objects.get(id=id_professor);
    return str(professor.first_name)+" "+str(professor.last_name)