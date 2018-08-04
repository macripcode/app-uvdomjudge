import time
from django import forms
from django.forms import ModelForm
from .models import Rubric


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



class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ['terminal_objetive','activity','weight', 'problem_id', 'contest_id']
        widgets = {
            'terminal_objetive': forms.Textarea,
            'activity': forms.Textarea,
        }

