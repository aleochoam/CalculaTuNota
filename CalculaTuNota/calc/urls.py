from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/(?P<user>.+)/(?P<subject>.+)/extra/$', views.notaFaltante),
    url(r'^api/(?P<user>.+)/(?P<subject>.+)/$', views.GradeList.as_view()),
    url(r'^api/(?P<user>.+)/$', views.UserSubjectList.as_view()),

    url(r'^createAccount/$', views.UserRegisterView.as_view(), name="createAccount"),
    url(r'^login/$', views.UserLogView.as_view(), name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),

    url(r'^user/(?P<subject>.+)/addGrades/$', views.addGrades, name='addGrades'),
    url(r'^user/(?P<subject>.+)/$', views.grades, name='grades'),
    url(r'^user/$', views.user, name="user"),

    # url(r'^users/$', views.all_users, name='all_users'),
    # url(r'^(?P<user>.+)/addSubject_submit/$', views.addSubject_submit, name='addSubject_submit'),
    # url(r'^(?P<user>.+)/addSubject/$', views.addSubject, name='addSubject'),
]
