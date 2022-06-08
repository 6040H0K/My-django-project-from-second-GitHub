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
    path('school/<int:id>', Show_school.as_view(), name = "school"),
    path('school/<int:id>/<int:id_class>', Show_class.as_view(), name = "clas"),
    path('school/<int:id>/<int:id_class>/lessons', Edit_lessons.as_view(), name = "lessons")
    
    # path(r'schools/(?P<id>[_\w+])$', show_school, name='school')
]

schools = School.objects.all()

