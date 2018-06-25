from django.conf.urls import url
from .views import professor_profile
from .views import page_created_course
from .views import page_fail_course
from .views import download_db_domjudge


urlpatterns = [
    url(r'^$', professor_profile),
    url(r'^created_course/', page_created_course, name='create_course'),
    url(r'^fail_course/', page_fail_course, name='fail_course'),
    url(r'^download_db/(?P<id_course>\d{12}M\d{2})/', download_db_domjudge, name='download_db'),
    #url(r'^(?P<pk>\d{1})/$', views.image_detail),
]