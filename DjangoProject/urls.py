"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from MainApp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Auth.as_view()),
    path('home/', home, name = 'home'),
    path('school/<int:id_school>/home_page/', home, name = 'home_page'),
    path('schools/', Schoolswork.as_view(), name = "schools"),
    path('school/<int:id>/', Show_school.as_view(), name = "school"),
    # path('school/<int:id>/<int:id_class>/lessons/', Edit_lessons.as_view(), name = "lessons_class"), ------------
    path('school/<int:id>/clases/<int:id_class>/marks/<int:month>/type=<int:type_page>/', Show_marks.as_view(), name = "marks"),
    path('school/<int:id>/clases/<int:id_class>/marks/<int:month>/student=<int:id_student>type=<int:type_page>/', Show_marks.as_view(), name = "marks"),
    path('school/<int:id>/clases/<int:id_class>/marks/<int:month>/lesson=<int:id_lesson>type=<int:type_page>/', Show_marks.as_view(), name = "marks"),
    path('auth/', Auth.as_view(), name='auth'),
    path('auth/<int:type_page>/', Auth.as_view(), name='auth'), 
    # path('school/<int:id>/lesson/<int:id_lesson>/', Teacher_class_page.as_view(), name='teacher_class_page'), ------------
    path('school/<int:id_school>/teachers/', Teachers.as_view(), name='teachers'),
    path('school/<int:id_school>/teachers/<int:id_teacher>/', Teacher_show.as_view(), name='teacher'),
    path('school/<int:id_school>/teachers/<int:id_teacher>/schadult/<str:day>', Teacher_schadult.as_view(), name='teacher'),
    path('school/<int:id_school>/lessons/', Lessons.as_view(), name='lessons'),
    path('school/<int:id_school>/lessons/<int:id_lesson>', Lesson_show.as_view(), name='lesson'),
    path('school/<int:id_school>/clases/', Clases.as_view(), name = 'clases'),
    path('school/<int:id_school>/students/', Students.as_view(), name = 'students'),
    path('school/<int:id_school>/students/<int:id_student>/', Student_show.as_view(), name = 'student'),
    # path('school/<int:id_school>/clases/<int:id_class>/students/<int:id_student>', Student_show.as_view(), name = 'student'),
    path('school/<int:id>/info/', School_info.as_view(), name = "school_info"),
    path('school/<int:id>/contacts/', School_contacts.as_view(), name = "school_contacts"),
    path('school/<int:id_school>/clases/<int:id_class>/', Class.as_view(), name = 'class'),
    path('school/<int:id_school>/clases/<int:id_class>/lessons/', Class_lessons.as_view(), name = 'class_lessons'),
    path('school/<int:id_school>/clases/<int:id_class>/students/', Class_students.as_view(), name = 'class_students'),
    path('school/<int:id_school>/clases/<int:id_class>/schadult/<str:day>/', Schadult.as_view(), name = 'schadult'),
    path('school/<int:id_school>/clases/<int:id_class>/schadult/<str:day>/<str:edit>/', Schadult.as_view(), name = 'edit_schadult'),
    path('school/<int:id_school>/info_site/<str:type_info>/', Info.as_view(), name = "info"),
    # path('school/<int:id>/lesson/<int:id_lesson>/<int:id_class>', Show_lesson_marks.as_view(), name='Show_lesson_marks') ------------
    
    # path(r'schools/(?P<id>[_\w+])$', show_school, name='school')
]