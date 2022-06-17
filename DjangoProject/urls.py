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
    path('', home),
    path('home/', home, name = 'home'),
    path('registration/', RegisterUser.as_view(), name = 'reg'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('make/', MakeSchool.as_view(), name = 'make'),
    path('schools/', Schoolswork.as_view(), name = "schools"),
    path('info/', info, name = 'info'),
    path('school/<int:id>', Show_school.as_view(), name = "school"),
    path('school/<int:id>/<int:id_class>', Show_class.as_view(), name = "clas"),
    path('school/<int:id>/<int:id_class>/lessons', Edit_lessons.as_view(), name = "lessons"),
    path('school/<int:id>/<int:id_class>/schadult', Edit_schadult.as_view(), name = "schadult"),
    path('school/<int:id>/<int:id_class>/info', Edit_info.as_view(), name = "info"),
    path('school/<int:id>/<int:id_class>/makestudent', Make_student.as_view(), name = "makestudent"),
    path('school/<int:id>/<int:id_class>/<int:id_student>/marks', Show_student_marks.as_view(), name = "studentmarks"),
    path('auth/', Auth.as_view(), name='auth'),
    path('auth/<int:type_page>', Auth.as_view(), name='auth'),
    path('school/<int:id>/teacher/<int:id_teacher>/', Teacher_page.as_view(), name='teacher_page'),
    path('school/<int:id>/lesson/<int:id_lesson>', Teacher_class_page.as_view(), name='teacher_class_page'),
    path('school/<int:id>/lesson/<int:id_lesson>/<int:id_class>', Show_lesson_marks.as_view(), name='Show_lesson_marks')
    
    # path(r'schools/(?P<id>[_\w+])$', show_school, name='school')
]

schools = School.objects.all()

