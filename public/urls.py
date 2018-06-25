from django.conf.urls import url
from .views import public_page
from .views import enroll_course


urlpatterns = [
    url(r'^$', public_page, name='public_page'),
    url(r'^(?P<id_course>\d{12}M\d{2})/enroll/$', enroll_course, name='enroll_course'),

]