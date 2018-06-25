from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from login.views import login_view
from login.views import logout_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^uvdomjudge/', include('public.urls')),
    url(r'^uvdomjudge/login/',login_view ),
    url(r'^uvdomjudge/logout/',logout_view ),
    url(r'^uvdomjudge/professor/', include('professor.urls')),
    url(r'^uvdomjudge/administrator/', include('administrator.urls')),

# urls api
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

   #login

]
