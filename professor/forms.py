import time
from django import forms


CODE_SUBJECTS_CHOICES = (
    ('0', 'Choose your option'),
    ('750001M', '750001M'),
    ('750017M', '750017M'),
)

NAMES_SUBJECTS_CHOICES = (
    ('0', 'Choose your option'),
    ('Algoritmia y Programación', 'Algoritmia y Programación'),
    ('Métodos Numéricos', 'Métodos Numéricos'),
)

CREDITS_SUBJECTS_CHOICES = (
    ('0', 'Choose your option'),
    ('3', '3'),
    ('4', '4'),
)


PERIOD_CHOICES = (
    ('0', 'Choose your option'),
    ('01', 'February - June'),
    ('02', 'August - December'),
)

current_year = time.strftime("%Y")


YEAR_CHOICES = (
    ('0', 'Choose your option'),
    (current_year, current_year),
)

LANGUAGES_CHOICES = (
    ('0', 'Choose your option'),
    ('1', 'Python'),
    ('2', 'Scilab'),
)


class CreateCourseForm(forms.Form):

    code_course = forms.ChoiceField(widget=forms.Select(),choices=CODE_SUBJECTS_CHOICES)
    name_course = forms.ChoiceField(widget=forms.Select(),choices=NAMES_SUBJECTS_CHOICES)
    credits_course = forms.ChoiceField(widget=forms.Select(),choices=CREDITS_SUBJECTS_CHOICES)
    professor_course = forms.CharField(max_length=50)
    group_course = forms.IntegerField(max_value=100)
    period_course = forms.ChoiceField(widget=forms.Select(),choices=PERIOD_CHOICES)
    year_course = forms.ChoiceField(widget=forms.Select(),choices=YEAR_CHOICES)
    programming_language = forms.ChoiceField(widget=forms.Select(),choices=LANGUAGES_CHOICES)


class ConfigProfileForm(forms.Form):
    id_user = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)




