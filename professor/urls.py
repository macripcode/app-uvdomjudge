from django.conf.urls import url
from .views import professor_profile
from .views import page_created_course
from .views import page_fail_course
from .views import download_db_domjudge
from .views import play_container
from .views import stop_container
from .views import remove_container
from .views import logs_container
from .views import course_profile
from .views import save_rubric
from .views import check_rubric



urlpatterns = [
    url(r'^$', professor_profile),
    url(r'^created_course/', page_created_course, name='create_course'),
    url(r'^fail_course/', page_fail_course, name='fail_course'),
    url(r'^download_db/(?P<id_course>\d{12}M\d{2})/', download_db_domjudge, name='download_db'),
    url(r'^play_container/', play_container, name='play_container'),
    url(r'^stop_container/', stop_container, name='stop_container'),
    url(r'^remove_container/', remove_container, name='remove_container'),
    url(r'^logs_container/', logs_container, name='logs_container'),
    url(r'^(?P<id_course>\d{12}M\d{2})/course/$', course_profile, name='course_profile'),
    url(r'^(?P<id_course>\d{12}M\d{2})/course/save_rubric/', save_rubric, name='save_rubric'),
    url(r'^(?P<id_course>\d{12}M\d{2})/course/check_rubric/', check_rubric, name='check_rubric'),
    #url(r'^(?P<pk>\d{1})/$', views.image_detail),
#url(r'^play_container/(?P<id_course>\d{12}M\d{2})/', play_container, name='play_container'),
]