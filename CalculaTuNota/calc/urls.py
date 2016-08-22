from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users$', views.all_users, name='all_users'),
    url(r'^createAccount$', views.createAccount, name='createAccount'),
    url(r'^createAccount.submit$', views.createAccount_submit, name='createAccount_submit'),
    url(r'^login$', views.login, name='login'),
    url(r'^login.submit$', views.login_submit, name='login_submit'),
    url(r'^(?P<user>.+)/(?P<subject>.+)/addGrades', views.addGrades, name='addGrades'),
    url(r'^(?P<user>.+)/(?P<subject>.+)$', views.grades, name='grades'),
    url(r'^(?P<user>.+)$', views.user, name='user'),
]