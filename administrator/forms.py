from django import forms


TYPE_USER_CHOICES = (
    ('0', 'Choose your option'),
    ('1', 'Administrator'),
    ('2', 'Professor'),
)


class CreateUserForm(forms.Form):
    type_user = forms.ChoiceField(widget=forms.Select(), choices=TYPE_USER_CHOICES)
    username = forms.CharField(label='Username')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField()
    id = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput())


