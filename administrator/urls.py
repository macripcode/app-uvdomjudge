from django.conf.urls import url
from .views import administrator_profile
from .views import page_created_user
from .views import page_fail_user
from .views import create_backups
from .views import created_backups_success
from .views import created_backups_fail



urlpatterns = [
    url(r'^$', administrator_profile),
    url(r'^created_user/', page_created_user, name='create_user'),
    url(r'^fail_user/', page_fail_user, name='fail_user'),
    url(r'^create_backups/', create_backups, name='create_backups'),
    url(r'^created_backups_success/', created_backups_success, name='create_user'),
    url(r'^created_backups_fail/', created_backups_fail, name='fail_user'),
]

