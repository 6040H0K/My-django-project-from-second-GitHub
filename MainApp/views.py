from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import*
# from DjangoProject import urls
day = 0
# Create your views here.
# print(urls.urlpatterns)
def home(request):
    return render(request, 'MainApp/home.html')
class Schoolswork(TemplateView):
    template_name = "MainApp/schools.html"
    id = -1
    def dispatch(self, request):
        school = School.objects.all()
        if request.method == "POST":
            self.id = request.POST.get('id')
            return redirect('/school/' + str(self.id))
            # return redirect("school")
        # print(people[0].title

    # print(len(school), '--------------------------------------')
        return render(request, self.template_name, context= {"school": school, 'range': school})
class Show_school(TemplateView):
    
    template_name = "MainApp/school.html"
    
    days = ['Понеділок', "Вівторок", "Середа" ,"Четвер", "П'ятниця"]
    type_page = ''
    range_cycle = 0
    
    
    def dispatch(self, request, id):
        global day
        # id_str = ''
        # id = str(request)
        # n = -3
        # while 1:
        #     id_str += id[n]
        #     n -= 1
        #     if id[n] == '/':
        #         break
        # id = int(id_str[::-1])
        # print(id)
        for i in range(len(School.objects.all())):
            if School.objects.all()[i].id == id:
                id = i
        school = School.objects.all()[id]
        if request.method == 'POST':
            
            if request.POST.get("id") == 'Створити клас':
                self.type_page = 'create_class'
            elif request.POST.get("id") == 'Створити урок':
                self.type_page = 'create_lesson'
            # print(request.POST.get("id"))
            # print(type_page)
            elif request.POST.get("id") == "Підтвердити" :

                rank = request.POST.get('rank')
                class_teacher = request.POST.get('class_teacher')
                name = request.POST.get('name')
                if rank and class_teacher and name:
                    clas = school.class_form.copy()
                    clas['rank'] = rank
                    clas['class_teacher'] = class_teacher
                    clas['name'] = name
                    if len(school.clases['clases']) > 0:
                        clas['ID'] = school.clases['clases'][-1]['ID'] + 1
                    else:
                        clas['ID'] = 0
                    school.clases['clases'].append(clas)
                    school.save()
            elif request.POST.get('id') == 'Перегляд класів':
                self.type_page = 'show_clases'
                self.range_cycle = school.clases['clases']
            elif request.POST.get('id') == '<':
                self.type_page = 'show_clases'
                self.range_cycle = school.clases['clases']
                day -= 1
                if day == -1:
                    day = 4
            elif request.POST.get('id') == '>':
                self.type_page = 'show_clases'
                self.range_cycle = school.clases['clases']
                day += 1
                if day == 5:
                    day = 0
            return render(request, self.template_name, 
                        context= {'school': school, 'type': self.type_page, 
                                'range': self.range_cycle, 'day': self.days[day]})
        else:
            return render(request, self.template_name, 
                        context= {'school': school, 'type': self.type_page, 
                                'range': self.range_cycle, 'day': self.days[day]})
    # except:
    #     print('error')
    #     return render(request, template_name)
    
def about(request):
    return render(request,"MainApp/about.html")
class RegisterUser(TemplateView):
    template_name = "MainApp/registration.html"
    errortext = 0
    def dispatch(self, request):
        if request.method == "POST":
            # print(request.POST)
            username = request.POST.get("User_Name") 
            password0 = request.POST.get("Password") 
            password_1 = request.POST.get("Password1") 
            email = request.POST.get("Email")
            if password0 == password_1:
                try:
                    User.objects.create_user(username,email,password0) #
                    return redirect("home")
                    self.errortext = 0 
                except:
                    pass
            else: 
                self.errortext = "Паролі не співпадають!" 
        return render(request, self.template_name, context= {"errortext": self.errortext})
class MakeSchool(TemplateView):
    template_name = "MainApp/make-school.html"
    errortext = 0
    def dispatch(self, request):
        
        self.errortext = 0
        a = {'errortext': self.errortext}
        
        
        if request.method == "POST":
            school = School()
            school.title = request.POST.get("name") 
            school.number = request.POST.get("num") 
            school.town = request.POST.get("town") 
            school.password = request.POST.get("password")
            school.lesson_form = {'name': '',
                                'teacher': ''}
            school.class_form = {'ID': -1,
                                'rank': -1,
                                'class_teacher': '',
                                'name': 'a',
                                'lessons_list': [],
                                'schedult': {'Mon': ['','','','','','','',''],
                                            'Tue': ['','','','','','','',''],
                                            'Wed': ['','','','','','','',''],
                                            "Thr": ['','','','','','','',''],
                                            "Fri": ['','','','','','','','']
                                            }
                                }
            school.clases = {'clases':[]}
            school.lessons = {'lessons':[]}
            
            school.save()
            return redirect("schools")
            # schools = School.objects.all()
            # new_school_url(schools[-1].id)
            self.errortext = 1
            # print(school.clases)
            # print(type(school.clases))
        return render(request, self.template_name, context={})
class LoginView(TemplateView):
    template_name = "MainApp/login.html"
    #
    errortext = 0
    def dispatch(self, request):
        #
        if request.method == "POST":
            self.errortext = 0
            username = request.POST.get("user_name")
            password1 = request.POST.get("password_1")
            #
            user = authenticate(request, username = username, password = password1)
            if user is not None:
                #
                login(request, user)
                #
                return redirect("home") 
                self.errortext = 0
            else:
                #
                self.errortext = "Логін або пароль введено невірно"
        #
        return render(request, self.template_name, context={"errortext": self.errortext})