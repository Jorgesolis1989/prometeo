"""PROMETEO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from usuarios import views
from django.contrib.auth.views import logout


urlpatterns = [
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.login_user, name="login_user"),
    url(r'^logout', logout,  {'next_page': '/'}, name='logout'),
    url(r'^register_user', views.registro_usuario, name="register_user"),
    url(r'^update_user', views.actualizar_usuario, name="update_user"),
    url(r'^change_password', views.cambio_contrasena, name="change_password"),
    url(r'^reset/password_reset/$', 'django.contrib.auth.views.password_reset', name='reset_password_reset1'),
    url(r'^reset/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^usuarios/$', include('usuarios.urls')),
    url(r'^register_user', views.registro_usuario, name="register_user"),
    url(r'^register_success/', views.confirmar_registro),
    url(r'^activate/(?P<activation_key>\w+)/',views.confirmar_registro, name="register_confirm"),
]
