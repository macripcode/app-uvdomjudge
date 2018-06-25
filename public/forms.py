from django import forms


class RegistrationForm(forms.Form):
    code_student = forms.CharField(max_length=50)
    name_student = forms.CharField(max_length=50)
    lastname_student = forms.CharField(max_length=50)
    email_student = forms.EmailField()
