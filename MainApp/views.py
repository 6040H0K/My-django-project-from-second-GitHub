from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from .models import*
from datetime import datetime, date
from random import randint
# from DjangoProject import urls

# Create your views here.
# print(urls.urlpatterns)
def check_account(request,school_id = None):
    account = None
    if school_id:
        if request.user.is_superuser:
            account = {'value': request.user.username,'name':request.user.username, 'type_user':'admin'}
        elif request.user.has_perm("MainApp.show_school"):
            school = School.objects.get(pk = school_id)
            account = {'value': school.id, 'name':school.title, 'type_user':'school'}
        elif request.user.has_perm("MainApp.view_student"):
            student= Student.objects.get(login = request.user.username)
            account = {'value': student.id, 'name':student.name + ' ' + student.surname, 'type_user':'student'}
        elif request.user.has_perm("MainApp.teacher"):
            school = School.objects.get(pk = school_id)
            for i in school.teachers['teachers']:
                if i['login'] == request.user.username:
                    teacher = i
                    break
            account = {'value': teacher['ID'], 'name':teacher['name'], 'type_user':'teacher'}
    else:
        if request.user.is_superuser:
            account = {'value': request.user.username,'name':request.user.username, 'type_user':'admin'}
    return account
def buttons_menu(request, school_id = None, aut = True):
    if request.method == 'GET':
        if request.GET.get('button_id_menu') == '1':
            if school_id == None:
                return 'home'
            else:
                return '/school/' + str(school_id) +'/home_page'
        elif request.GET.get('button_id_menu') == '2':
            if school_id == None:
                return 'schools'
            else:
                return '/school/' + str(school_id)
        elif request.GET.get('button_id_menu') == '3':
            return '/school/' + str(school_id) + '/teachers'
        elif request.GET.get('button_id_menu') == '4':
            return '/school/' + str(school_id) + '/students'
        elif request.GET.get('button_id_menu') == '5':
            
            if request.user.has_perm('MainApp.view_student') and not request.user.is_superuser:
                student = Student.objects.get(login = request.user.username)
                for i in School.objects.get(pk = school_id).clases['clases']:
                    for k in i['students']:
                        if student.id == k:
                            temp = i
                            break
                return '/school/' + str(school_id) + '/clases/' + str(temp['ID'])
            else:
                return '/school/' + str(school_id) + '/clases'
        elif request.GET.get('button_id_menu') == '6':
            return '/school/' + str(school_id) + '/lessons'
        elif request.GET.get('button_id_menu') == '7':
            if school_id:
                return '/school/' + str(school_id) + '/info_site/about_us'
            else:
                return '/info_site/about_us'
        elif request.GET.get('button_id_menu') == '8':
            logout(request)
            return '/auth'
    if request.method == 'POST':
        if request.POST.get('account'):

            if request.POST.get('type_user') == 'teacher':

                return '/school/' + str(school_id) + '/teachers/' + str(request.POST.get('account'))
            elif request.POST.get('type_user') == 'student':

                return '/school/' + str(school_id) + '/students/' + str(request.POST.get('account'))
            elif request.POST.get('type_user') == 'school':

                return '/school/' + str(request.POST.get('account'))
            
            elif request.POST.get('type_user') == 'admin':
                return '/schools'
    if not request.user.is_authenticated and aut:
        return '/auth'
    
        
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
def home(request, id_school = None):
    tmp = buttons_menu(request, id_school, False)
    if tmp != None:
        return redirect(tmp)
    last_id_news = len(News.objects.all()) - 1
    if id_school:
        School.objects.get(pk = id_school)
        return render(request, 'MainApp/home.html', context={"select_menu":0,'news':News.objects.all()[last_id_news],
                     'account':check_account(request,id_school)})
    else:
        return render(request, 'MainApp/home.html', context={"select_menu":0,'type_menu':1,
        'news':News.objects.all()[last_id_news], 'account':check_account(request)})

class Show_marks(TemplateView):
    template_name = "MainApp/mark.html"
    
    def dispatch(self, request, id,id_class,month,type_page,id_student = None,id_lesson = None):
        student = None
        range1 = None
        lesson = None
        id_month = month
        tmp = buttons_menu(request, id)
        if type_page == 1:
            select_menu = 3
            menu_class_select = 7
        elif type_page == 2:
            select_menu = 4
            menu_class_select = 7
        elif type_page == 0:
            select_menu = 4
            menu_class_select = 7
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id)
        for i in school.clases['clases']:
            if int(i['ID']) == int(id_class):
                clas = i
        students = []
        for i in clas['students']:
            student = Student.objects.get(pk = i)
            students.append(student)
        student = None
        lessons = clas['lessons_list']
        if id_lesson != None:
            for i in lessons:
                if i['ID'] == id_lesson:
                    lesson = i
                    break
        monthes = [
            {'ID': 0, 'name':'Вересень'},
            {'ID': 1, 'name':'Жовтень'},
            {'ID': 2, 'name':'Листопад'},
            {'ID': 3, 'name':'Грудень'},
            {'ID': 4, 'name':'Січень'},
            {'ID': 5, 'name':'Лютий'},
            {'ID': 6, 'name':'Березень'},
            {'ID': 7, 'name':'Квітень'},
            {'ID': 8, 'name':'Травень'},
        ]
        month = monthes[month]
        month_for_html = ['09','10','11','12','01','02','03','04','05']
        if id_student != None and id_lesson != None:
            student = Student.objects.get(pk = id_student)
            range1 = student.marks[str(month['ID'])].copy()
            tmp = []
            for i in range1:
                if i['ID'] != lesson['ID']:
                    tmp.append(i)
            for i in tmp:
                range1.remove(i)
            for i in range1:
                for k in clas['lessons_list']:
                    if i['ID'] == k['ID'] and k['ID'] == lesson['ID']:
                        i['name'] = k['name']
                        break
            # print(range1)
        elif id_student != None:
            student = Student.objects.get(pk = id_student)
            range1 = student.marks[str(month['ID'])].copy()
            for i in range1:
                for k in clas['lessons_list']:
                    if i['ID'] == k['ID']:

                        i['name'] = k['name']
        elif id_lesson != None:
            range1 = []
            for j in clas['students']:
                stud = Student.objects.get(pk = j)
                for k in stud.marks[str(month['ID'])]:
                    if k['ID'] == lesson['ID']:
                        temp = k
                        temp['name'] = stud.name + ' ' + stud.surname
                        temp['stud_id'] = stud.id
                        range1.append(k)
        if request.method == 'POST':
            if request.POST.get('but_filtr') == '1':
                if request.POST.get('student') != 'null' and request.POST.get('lesson') != 'null':
                    if type_page == 1 or type_page == 2:
                        return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + request.POST.get('month') + '/student=' + str(request.POST.get('student')) + 'lesson=' + str(request.POST.get('lesson') + 'type=1'))
                    else:
                        return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + request.POST.get('month') + '/student=' + str(request.POST.get('student')) + 'lesson=' + str(request.POST.get('lesson') + 'type=0'))
                elif request.POST.get('student') != 'null':
                    if type_page == 1 or type_page == 2:
                        return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + request.POST.get('month') + '/student=' + str(request.POST.get('student') + 'type=1'))
                    else:
                        return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + request.POST.get('month') + '/student=' + str(request.POST.get('student') + 'type=0'))
                elif request.POST.get('lesson') != 'null':
                    if type_page == 1 or type_page == 2:

                        return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + request.POST.get('month') + '/lesson=' + str(request.POST.get('lesson') + 'type=2'))
                    else:
                        return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + request.POST.get('month') + '/lesson=' + str(request.POST.get('lesson') + 'type=0'))
            if request.POST.get('button_menu') == '1':
                if type_page == 0:
                    return redirect('/school/' + str(id) + '/clases/' + str(id_class))
                elif type_page == 2:
                    return redirect('/school/' + str(id) + '/lessons/' + str(id_lesson))
                elif type_page == 1:
                    return redirect('/school/' + str(id) + '/students/' + str(id_student))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/schadult/Mon')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/students/')
            elif request.POST.get('button_menu') == '4':
                return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/lessons/')
            elif request.POST.get('button_menu') == '7':
                if type_page == 0:
                    return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + "0/type=0")
                elif type_page == 1:
                    return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + "0/student="+ str(id_student) + "type=0")
            if request.POST.get('save_marks') == '1':
                if student != None and lesson != None:
                    for i in range(len(range1)):
                        for j in range(len(range1[i]['marks'])):
                            print(range1[i]['marks'])
                            student.marks[str(month['ID'])][i]['marks'][j]['mark'] = request.POST.get(str(range1[i]['ID'])+'-'+str(range1[i]['marks'][j]['ID']))
                    student.save()
                    return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/'  + str(month['ID']) +"/" + 'student=' + str(id_student) + 'lesson=' + str(id_lesson) + 'type=' + str(type_page))
                elif student != None:
                    for i in range(len(range1)):
                        for j in range(len(range1[i]['marks'])):
                            print(range1[i]['marks'])
                            student.marks[str(month['ID'])][i]['marks'][j]['mark'] = request.POST.get(str(range1[i]['ID'])+'-'+str(range1[i]['marks'][j]['ID']))
                    student.save()
                    return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/'  + str(month['ID']) +"/" + 'student=' + str(id_student) + 'type=' + str(type_page))
                elif lesson != None:
                    for i in range(len(range1)):
                        print(range1[i])
                        student = Student.objects.get(pk = range1[i]['stud_id'])
                        for j in range(len(range1[i]['marks'])):

                            student.marks[str(month['ID'])][lesson['ID']]['marks'][j]['mark'] = request.POST.get(str(range1[i]['stud_id'])+'-'+str(range1[i]['marks'][j]['ID']))
                        student.save()

                    return redirect('/school/' + str(id) + '/clases/' + str(id_class) + '/marks/' + str(month['ID']) +"/" + 'lesson=' + str(id_lesson) + 'type=' + str(type_page))

        return render(request, self.template_name, context={ 'students':students, 'lessons':lessons,
                     'class':clas, 'monthes':monthes, 'month':month,
                        'student':student, 'lesson':lesson, 'range':range1,'select_menu':select_menu,
                        'type_page':type_page, 'menu_class_select':menu_class_select, 'account':check_account(request,id),
                         'id_month':month_for_html[month['ID']]})

class Schoolswork(TemplateView):
    template_name = "MainApp/schools.html"
    id = -1
    errortext = 0
    def dispatch(self, request):
        make = False
        id_school_for_info_form = None
        tmp = buttons_menu(request)
        if tmp != None:
            return redirect(tmp)
        if request.user.is_superuser:
            info_for_edit = None
            if request.method == "POST":
                if request.POST.get('button_del'):
                    school = School.objects.get(pk = int(request.POST.get('button_del')))
                    try:
                        user = User.objects.get(username = school.login)
                        user.delete()
                    except:
                        pass
                    for i in school.teachers['teachers']:
                        try:
                            user_tmp = User.objects.get(username = i['login'])
                            user_tmp.delete()
                        except:
                            pass
                    
                    school.delete()
                elif request.POST.get('button_edit'):
                    school = School.objects.get(pk = int(request.POST.get('button_edit')))
                    make = 1
                    info_for_edit = school
                elif request.POST.get('make'):
                    make = 1
                elif request.POST.get('save_school'):
                    school = School.objects.get(pk = request.POST.get('save_school'))
                    school.title = request.POST.get("name") 
                    school.number = request.POST.get("num") 
                    school.town = request.POST.get("town") 
                    school.password = request.POST.get("password")
                    user = User.objects.get(username = school.login)
                    school.login = request.POST.get('email')
                    school.email = request.POST.get('email')
                    user.username = school.login
                    user.set_password(school.password) 
                    user.save()
                    school.school_site = request.POST.get('site')
                    school.school_phone = request.POST.get('phone')
                    info_for_edit = school
                    make = 2
                    school.save()
                elif request.POST.get('save_school1'):
                    school = School.objects.get(pk = request.POST.get('save_school1'))
                    school.adress = request.POST.get('adress')
                    school.school_type =  request.POST.get('school_type')
                    school.school_director =  request.POST.get('director')
                    school.school_profil = request.POST.get('profil')
                    school.facebook = request.POST.get('facebook')
                    school.instagram = request.POST.get('instagram')
                    school.save()
                elif request.POST.get('new_school'):
                    school = School.objects.get(pk = request.POST.get('school_id'))
                    school.adress = request.POST.get('adress')
                    school.school_type =  request.POST.get('school_type')
                    school.school_director =  request.POST.get('director')
                    school.school_profil = request.POST.get('profil')
                    school.facebook = request.POST.get('facebook')
                    school.instagram = request.POST.get('instagram')
                    school.save()
                elif request.POST.get('next1'):
                    # errortext = 0
                    # a = {'errortext': self.errortext}
                    school = School()
                    
                    school.title = request.POST.get("name") 
                    school.number = request.POST.get("num") 
                    school.town = request.POST.get("town") 
                    school.login = request.POST.get('email')
                    school.email = request.POST.get('email')
                    school.password = request.POST.get("password")
                    school.school_site = request.POST.get('site')
                    school.school_phone = request.POST.get('phone')
                    
                    if school.title and school.number and school.town and school.password and request.POST.get('site') and request.POST.get('phone'):
                        school.lesson_form = {'name': '',
                                            'teacher': '',
                                            'ID': -1}
                        school.class_form = {'ID': -1,
                                            'rank': -1,
                                            'students': [],
                                            'class_teacher': '',
                                            'name': 'a',
                                            'lessons_list': [],
                                            'schedult': {'Mon': [{'name': '', 'num': '1'},
                                                                {'name': '', 'num': '2'},
                                                                {'name': '', 'num': '3'},
                                                                {'name': '', 'num': '4'},
                                                                {'name': '', 'num': '5'},
                                                                {'name': '', 'num': '6'},
                                                                {'name': '', 'num': '7'},
                                                                {'name': '', 'num': '8'}],
                                                        'Tue': [{'name': '', 'num': '1'},
                                                                {'name': '', 'num': '2'},
                                                                {'name': '', 'num': '3'},
                                                                {'name': '', 'num': '4'},
                                                                {'name': '', 'num': '5'},
                                                                {'name': '', 'num': '6'},
                                                                {'name': '', 'num': '7'},
                                                                {'name': '', 'num': '8'}],
                                                        'Wed': [{'name': '', 'num': '1'},
                                                                {'name': '', 'num': '2'},
                                                                {'name': '', 'num': '3'},
                                                                {'name': '', 'num': '4'},
                                                                {'name': '', 'num': '5'},
                                                                {'name': '', 'num': '6'},
                                                                {'name': '', 'num': '7'},
                                                                {'name': '', 'num': '8'}],
                                                        "Thr": [{'name': '', 'num': '1'},
                                                                {'name': '', 'num': '2'},
                                                                {'name': '', 'num': '3'},
                                                                {'name': '', 'num': '4'},
                                                                {'name': '', 'num': '5'},
                                                                {'name': '', 'num': '6'},
                                                                {'name': '', 'num': '7'},
                                                                {'name': '', 'num': '8'}],
                                                        "Fri": [{'name': '', 'num': '1'},
                                                                {'name': '', 'num': '2'},
                                                                {'name': '', 'num': '3'},
                                                                {'name': '', 'num': '4'},
                                                                {'name': '', 'num': '5'},
                                                                {'name': '', 'num': '6'},
                                                                {'name': '', 'num': '7'},
                                                                {'name': '', 'num': '8'}]
                                                        }
                                            }
                        school.teachers = {'teachers': []}
                        school.clases = {'clases':[]}
                        school.lessons = {'lessons':[]}

                        
                        school.save()
                        id_school_for_info_form = school.id
                        print(id_school_for_info_form)
                        user = User.objects.create_user(
                            username=school.login,
                            email=school.email,
                            password=school.password
                        )
                        permission = Permission.objects.get(codename='show_school')
                        user.user_permissions.add(permission)
                        user.save()
                        make = 2
                    else:
                        make = 1
                        # self.errortext = 1
                elif request.POST.get('id'):
                    self.id = request.POST.get('id')
                    return redirect('/school/' + str(self.id))
                # return redirect("school")
            # print(people[0].title
            school = School.objects.all()
        # print(len(school), '--------------------------------------')
            return render(request, self.template_name, context= {"school": school, 'range': school, 'make':make,
                        'select_menu':1, 'type_menu':1, 'info_for_edit':info_for_edit, 'account':check_account(request,None),
                        'id_school_for_info_form':id_school_for_info_form})
        else:
            if request.user.is_authenticated:
                logout(request)
            return redirect('/auth')
class Student_show(TemplateView):
    template_name = "MainApp/student.html"
    def dispatch(self,request,id_school,id_student, id_class = None):
        tmp = buttons_menu(request, id_school)
        school = School.objects.get(pk = id_school)
        clas = None
        if tmp != None:
            return redirect(tmp)
        if id_class != None:
            type_page = 1
            select_menu = 4
            menu_class_select = 3
            id_class_for_redirect = id_class
            for i in range(len(school.clases['clases'])):
                if int(school.clases['clases'][i]['ID']) == int(id_class):
                    id_class = i
            clas = school.clases['clases'][id_class]
            if request.method == 'POST':
                if request.POST.get('button_menu') == '1':
                    return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect))
                elif request.POST.get('button_menu') == '2':
                    return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/Mon')
                elif request.POST.get('button_menu') == '3':
                    return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/students/')
                elif request.POST.get('button_menu') == '4':
                    return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/lessons/')
                
        else:
            if request.method == 'POST':
                if request.POST.get('button_menu') == '7':
                    for i in school.clases['clases']:
                        if id_student in i['students']:
                            id_class_for_redirect = i['ID']
                            break
                    return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/marks/0/student=' + str(id_student) + 'type=1')
            menu_class_select = 1
            type_page = None
            select_menu = 3
        
        
        
        student = Student.objects.get(pk = id_student)
        return render(request, self.template_name, context={'class':clas, 'menu_class_select':menu_class_select,
                                                            'select_menu':select_menu, 'type_page':type_page,
                                                            'student':student, 'account':check_account(request,id_school)
                                })
class Class_students(TemplateView):
    template_name = 'MainApp/class_students.html'
    def dispatch(self,request,id_school,id_class):
        tmp = buttons_menu(request, id_school)
        id_class_for_redirect = id_class
        make = None
        id_student_for_parents_form = None
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id_school)
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/Mon')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/students/')
            elif request.POST.get('button_menu') == '4':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/lessons/')
            elif request.POST.get('button_menu') == '7':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/marks/' + "0/type=0")
        clas = school.clases['clases'][id_class]
        students = clas['students']
        students_range = []
        for i in students:
            students_range.append(Student.objects.get(pk = i))
        
        if request.method == 'POST':
            if request.POST.get('make'):
                make = 1
            elif request.POST.get('button_del'):
                school.clases['clases'][id_class]['students'].remove(int(request.POST.get('button_del')))
                school.save()
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/students/')
            elif request.POST.get('id'):
                id = request.POST.get('id')
                return redirect('/school/' + str(id_school) + '/students/' + str(id))
            elif request.POST.get('new_student'):
                print(request.POST.get('student_id'))
                student = Student.objects.get(pk = int(request.POST.get('student_id')))
                student.name_parrent1 = request.POST.get('name_parrent1')
                student.number_phone_parrent1 = request.POST.get('number_phone_parrent1')
                student.work_parrent1 = request.POST.get('work_parrent1')
                student.name_parrent2 = request.POST.get('name_parrent2')
                student.number_phone_parrent2 = request.POST.get('number_phone_parrent2')
                student.work_parrent2 = request.POST.get('work_parrent2')
                student.save()
            elif request.POST.get('next1'):
                make = 2
                try:
                # print(1)
                    if request.POST.get("birthday"):
                        # print(2)
                        Student.objects.create(
                            name = request.POST.get('name'),
                            surname = request.POST.get('surname'),
                            second_name = request.POST.get('second_name'),
                            birthday = request.POST.get('birthday'),
                            age = str(calculate_age(datetime.strptime(request.POST.get('birthday'), "%Y-%m-%d"))),
                            login = request.POST.get('email'),
                            marks = {
                                0:[],
                                1:[],
                                2:[],
                                3:[],
                                4:[],
                                5:[],
                                6:[],
                                7:[],
                                8:[],
                            },
                            password = str(randint(10000000,99999999)),
                            email = request.POST.get('email'),
                            number_phone = request.POST.get('number_phone'),
                            adress = request.POST.get('adress'),
                            name_parrent1 = '',
                            number_phone_parrent1 = '',
                            work_parrent1 = '',
                            name_parrent2 = '',
                            number_phone_parrent2 = '',
                            work_parrent2 = ''
                        )
                        
                        for clas_num in school.clases['clases']:
                            # print(clas_num['ID'], request.POST.get('class_stud'))
                            if str(clas_num['ID']) == request.POST.get('class_stud'):
                                id_class = school.clases['clases'].index(clas_num)
                        temp = school.clases['clases'][id_class].keys()
                        temp1 = len(Student.objects.all())
                        student = Student.objects.all()[temp1 - 1]
                        temp_list = []
                        marks_temp = []
                        for el in range(30):
                            marks_temp.append({'ID': el,"mark": ' '})
                        for j in school.clases['clases'][id_class]['lessons_list']:
                            temp_list.append({'ID':j['ID'],'marks':marks_temp})
                        for i in student.marks.keys():
                            student.marks[i] = temp_list
                        student.save()
                        id_student_for_parents_form = str(Student.objects.all()[len(Student.objects.all()) - 1].id)
                        # print(id_student_for_parents_form)
                        if 'students' in temp:
                            school.clases['clases'][id_class]['students'].append(Student.objects.all()[temp1-1].id)
                        else:
                            school.clases['clases'][id_class]['students'] = [Student.objects.all()[temp1-1].id]
                        # print(3)
                        school.save()
                        user = User.objects.create_user(
                            username=student.login,
                            email=student.email,
                            password=student.password
                        )
                        permission = Permission.objects.get(codename='view_student')
                        user.user_permissions.add(permission)
                        user.save()
                    
                    else:
                        self.error_text = 'Заповніть усі поля'
                except:

                    self.error_text = 'Заповніть усі поля'
                        
        return render(request, self.template_name, context={'class':clas, 'menu_class_select':3,
                                                            'select_menu':4, 'range':students_range,
                                                            'make':make, 'id_student_for_parents_form':id_student_for_parents_form,
                                                            'account':check_account(request,id_school)
                                })
class Class_lessons(TemplateView):
    template_name = 'MainApp/class_lessons.html'
    def dispatch(self,request,id_school,id_class):
        tmp = buttons_menu(request, id_school)
        id_class_for_redirect = id_class
        make = None
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id_school)
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/Mon')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/students/')
            elif request.POST.get('button_menu') == '4':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/lessons/')
            elif request.POST.get('button_menu') == '7':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/marks/' + "0/type=0")
        clas = school.clases['clases'][id_class]
        lessons = clas['lessons_list']
        lessons_range = school.lessons['lessons']
        if request.method == 'POST':
            if request.POST.get('make'):
                make = True
            elif request.POST.get('button_del'):
                for i in clas['lessons_list']:
                    if i['ID'] == int(request.POST.get('button_del')):
                        school.clases['clases'][id_class]['lessons_list'].remove(i)
                        for stud in Student.objects.all():
                            if stud.id in school.clases['clases'][id_class]['students']:
                                name = i['name']
                                for j in stud.marks.keys():
                                    for k in stud.marks[j]:
                                        if k['ID'] == i['ID']:
                                            stud.marks[j].remove(k)
                                stud.save() 
                        break
                school.save()
            elif request.POST.get('id'):
                id = request.POST.get('id')
                return redirect('/school/' + str(id_school) + '/lessons/' + str(id))
            elif request.POST.get('new_lesson'):
                for i in school.lessons['lessons']:
                    if i['ID'] == int(request.POST.get('lesson')):
                        
                        school.clases['clases'][id_class]['lessons_list'].append(i)
                        for stud in Student.objects.all():
                            if stud.id in school.clases['clases'][id_class]['students']:
                                name = i['name']
                                marks_temp = []
                                for el in range(30):
                                    marks_temp.append({'ID': el,"mark": ' '})

                                for j in stud.marks.keys():
                                    stud.marks[j].append({'ID':i['ID'],'marks':marks_temp})
                                stud.save() 
                        break
                school.save()
        return render(request, self.template_name, context={'class':clas, 'menu_class_select':4,
                                                            'select_menu':4, 'lessons':lessons,
                                                            'make':make, 'lessons_range':lessons_range, 'account':check_account(request,id_school)
                                })
class Class(TemplateView):
    template_name = "MainApp/class.html"
    def dispatch(self,request,id_school,id_class):
        tmp = buttons_menu(request, id_school)
        id_class_for_redirect = id_class
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id_school)
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/Mon')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/students/')
            elif request.POST.get('button_menu') == '4':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/lessons/')
            elif request.POST.get('button_menu') == '7':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/marks/' + "0/type=0")
        clas = school.clases['clases'][id_class]
        return render(request, self.template_name, context={'class':clas, 'menu_class_select':1,
                                                            'select_menu':4, 'account':check_account(request,id_school)
                                })

class Auth(TemplateView):
    template_name = "MainApp/auth.html"
    type_page = 'start'
    def dispatch(self, request, type_page = None):
        error_text = 0
        tmp = buttons_menu(request,aut=False)
        if request.user.is_authenticated:
            logout(request)
        if tmp != None:
            return redirect(tmp)
        if type_page != None:
            self.type_page = str(type_page)
        if request.method == 'POST':
            if request.POST.get('button_choise') != None:
                return redirect('/auth/' + request.POST.get('button_choise'))
            if request.POST.get('submit') == 'teacher':
                try:
                    school = School.objects.get(pk = int(request.POST.get('school_name')))
                except:
                    school = None
                if school != None:

                    user = authenticate(username = request.POST.get('login'), password = request.POST.get('password'))
                else:
                    user = None
                if user is not None:
                    if user.is_active and user.has_perm('MainApp.teacher'):
                        print(2)
                        for i in school.teachers['teachers']:
                            if i['login'] == request.POST.get('login'):
                                login(request, user)
                                return redirect('/school/' + str(school.id) + '/teachers/' + str(i['ID']))
            if request.POST.get('submit') == 'student':
                try:
                    school = School.objects.get(pk = int(request.POST.get('school_name')))
                except:
                    school = None
                if school != None:

                    user = authenticate(username = request.POST.get('login'), password = request.POST.get('password'))
                else:
                    user = None
                if user is not None:
                    if user.is_active and user.has_perm('MainApp.view_student'):
                        print(2)
                        try:
                            student = Student.objects.get(login = request.POST.get('login'))
                        except:
                            student = None
                        if student != None:
                            login(request, user)
                            return redirect('/school/' + str(school.id) + '/students/' + str(student.id))
            if request.POST.get('submit') == 'school':
                user = authenticate(username = request.POST.get('login'), password = request.POST.get('password'))
                if user is not None:
                    if user.is_active and user.has_perm('MainApp.show_school'):
                        login(request, user)
                        return redirect('/school/' + str(School.objects.get(login = request.POST.get('login')).id))
            if request.POST.get('submit') == 'admin':
                user = authenticate(username = request.POST.get('login'), password = request.POST.get('password'))
                if user is not None:
                    if user.is_active and user.is_superuser:
                        login(request, user)
                        return redirect('/schools')
        return render(request, self.template_name, context ={
            'type_page':self.type_page, 'school_range':School.objects.all(),
            'error_text':error_text, 'select_menu':7
        })


class Lesson_show(TemplateView):
    template_name = "MainApp/lesson.html"
    def dispatch(self,request,id_school,id_lesson):
        tmp = buttons_menu(request, id_school)
        make = None
        
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id_school)
        for i in school.lessons['lessons']:
            if i['ID'] == id_lesson:
                lesson = i
                break
        if request.method == 'POST':
            if request.POST.get('view'):
                return redirect('/school/' + str(id_school) + '/clases/' + str(request.POST.get('view')) + '/marks/0/lesson=' + str(id_lesson) + 'type=2')
        clases = []
        for i in school.clases['clases']:
            if lesson in i['lessons_list']:
                clases.append(i) 
        return render(request, self.template_name, 
                        context={'school':school,
                                'lesson':lesson,
                                'clases':clases,
                                'select_menu':5,
                                'menu_class_select':1,
                                'account':check_account(request,id_school)
                                })
class Teacher_show(TemplateView):
    template_name = "MainApp/teacher.html"
    def dispatch(self,request,id_school,id_teacher):
        tmp = buttons_menu(request, id_school)
        make = None
        
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id_school)
        teacher_range = school.teachers['teachers']
        for i in school.teachers['teachers']:
            if i['ID'] == id_teacher:
                teacher = i
                break
        clases_list = []
        lessons_list = []
        for i in school.lessons['lessons']:
            try:
                if i['teacher']['ID'] == id_teacher:
                    lessons_list.append(i)
            except:
                pass
        for i in school.clases['clases']:
            try:
                if i['class_teacher']['ID'] == id_teacher:
                    clases_list.append(i)
            except:
                pass
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id_school) + '/teachers/' + str(id_teacher))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id_school) + '/teachers/' + str(id_teacher) + '/schadult/Mon')
            elif request.POST.get('view'):
                return redirect('/school/' + str(id_school) + '/clases/' + str(request.POST.get('view')))
            elif request.POST.get('view_lesson'):
                return redirect('/school/' + str(id_school) + '/lessons/' + str(request.POST.get('view_lesson')))
            elif request.POST.get('edit'):
                for i in school.clases['clases']:
                    if int(i['ID']) == int(request.POST.get('edit')):
                        make = i
                        break
            elif request.POST.get('save_school'):
                rank = request.POST.get('rank')
                class_teacher = request.POST.get('teacher')
                name = request.POST.get('name')
                for i in school.teachers['teachers']:
                    if str(i['ID']) == class_teacher:
                        class_teacher = i
                        break
                for i in school.clases['clases']:
                    if i['ID'] == int(request.POST.get('save_school')):
                        clas = school.clases['clases'].index(i)
                        break
                if rank and class_teacher != 'null' and name:
                    school.clases['clases'][clas]['rank'] = rank
                    school.clases['clases'][clas]['class_teacher'] = class_teacher
                    school.clases['clases'][clas]['name'] = name
                    school.save()
                    return redirect('/school/' + str(id_school) + '/teachers/' + str(id_teacher))
        return render(request, self.template_name, 
                        context={'school':school,
                                'teacher':teacher,
                                'clases': clases_list,
                                'lessons':lessons_list,
                                'select_menu':2,
                                'menu_class_select':1,
                                'make':make,
                                'teacher_range':teacher_range,
                                'account':check_account(request,id_school)})
class Teachers(TemplateView):
    template_name = "MainApp/teachers.html"
    range_cycle = 0
    error_text = None
    def dispatch(self, request ,id_school):
        tmp = buttons_menu(request, id_school)
        if tmp != None:
            return redirect(tmp)
        make = False
        school = School.objects.get(pk = id_school)
        self.range_cycle = school.teachers['teachers']
        info_for_edit = None
        if request.method == 'POST':
            if request.POST.get('make'):
                make = True
            elif request.POST.get('button_del'):
                for i in school.teachers['teachers']:
                    if i['ID'] == int(request.POST.get('button_del')):
                        user = User.objects.get(username = i['login'])
                        user.delete()
                        for k in school.clases['clases']:
                            try:
                                if k['class_teacher']['ID'] == i['ID']:
                                    k['class_teacher'] = ''
                            except:
                                pass
                        for k in school.lessons['lessons']:
                            try:
                                if k['teacher']['ID'] == i['ID']:
                                    k['teacher'] = ''
                            except:
                                pass
                        school.teachers['teachers'].remove(i)
                        school.save()
                        break
            if request.POST.get('button_edit'):
                make = True
                
                for i in school.teachers['teachers']:
                    if i['ID'] == int(request.POST.get('button_edit')):
                        teacher = i
                        break
                info_for_edit = teacher
            elif request.POST.get('save_teacher'):
                for i in school.teachers['teachers']:
                    print(i['ID'], int(request.POST.get('save_teacher')))
                    if i['ID'] == int(request.POST.get('save_teacher')):
                        teacher = school.teachers['teachers'].index(i)
                        break
                name = request.POST.get('name')
                login = request.POST.get('login')
                password = request.POST.get('password')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                user = User.objects.get(username = school.teachers['teachers'][teacher]['login'])
                user.username = login
                user.set_password(password)
                user.save()
                school.teachers['teachers'][teacher]['name'] = name
                school.teachers['teachers'][teacher]['login'] = login
                school.teachers['teachers'][teacher]['password'] = password
                school.teachers['teachers'][teacher]['email'] = email
                school.teachers['teachers'][teacher]['phone'] = phone
    
                school.save()
            elif request.POST.get('new_teacher'):
                name = request.POST.get('name')
                login = request.POST.get('login')
                password = request.POST.get('password')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                teacher = {}
                teacher['name'] = name
                teacher['login'] = login
                teacher['password'] = password
                teacher['email'] = email
                teacher['phone'] = phone
                if name and login and password and email and phone:
                    if len(school.teachers['teachers']) > 0:
                        teacher['ID'] = school.teachers['teachers'][-1]['ID'] + 1
                    else:
                        teacher['ID'] = 0
                    school.teachers['teachers'].append(teacher)
                    user = User.objects.create_user(
                        username=login,
                        email=email,
                        password=password
                    )
                    permission = Permission.objects.get(codename='teacher')
                    user.user_permissions.add(permission)
                    user.save()
                    school.save()
                    self.range_cycle = school.teachers['teachers']
                else:
                    make = True
                    self.error_text = 'Заповніть усі поля'
            elif request.POST.get('id'):
                id = request.POST.get('id')
                return redirect('/school/' + str(id_school) + '/teachers/' + str(id))
        return render(request, self.template_name, 
                    context= {'school': school,
                            'range': self.range_cycle,
                            'error': self.error_text, 'make':make,'select_menu': 2, 'info_for_edit':info_for_edit,
                            'account':check_account(request,id_school)})
class Lessons(TemplateView):
    template_name = "MainApp/lessons.html"
    range_cycle = 0
    error_text = None
    def dispatch(self, request, id_school):
        tmp = buttons_menu(request, id_school)
        if tmp != None:
            return redirect(tmp)
        make = False
        school = School.objects.get(pk = id_school)
        if request.user.has_perm('MainApp.show_school'):
            self.range_cycle = school.lessons['lessons']
        elif request.user.has_perm('MainApp.teacher'):
            self.range_cycle = []
            for i in school.teachers['teachers']:
                if i['login'] == request.user.username:
                    
                    for k in school.lessons['lessons']:
                        
                        if k['teacher']['ID'] == i['ID']:
                            self.range_cycle.append(k)
                    break
        teacher_range = school.teachers['teachers']
        info_for_edit = None
        if request.method == 'POST':
            if request.POST.get('make'):
                make = True
            elif request.POST.get('button_del'):
                for i in school.lessons['lessons']:
                    if i['ID'] == int(request.POST.get('button_del')):
                        school.lessons['lessons'].remove(i)
                        break
                for i in range(len(school.clases['clases'])):
                    for j in school.clases['clases'][i]['lessons_list']:
                        if j['ID'] == int(request.POST.get('button_del')):
                            school.clases['clases'][i]['lessons_list'].remove(j)
                school.save()
            elif request.POST.get('button_edit'):
                make = True
                for i in school.lessons['lessons']:
                    if i['ID'] == int(request.POST.get('button_edit')):
                        info_for_edit = i
                        break
            elif request.POST.get('save_lesson'):
                for i in school.lessons['lessons']:
                    if i['ID'] == int(request.POST.get('save_lessom')):
                        lesson = school.lessons['lessons'].index(i)
                        break
                name = request.POST.get('name')
                teacher = request.POST.get('teacher')
                for i in school.teachers['teachers']:
                    if str(i['ID']) == teacher:
                        teacher = i
                        break
                if name and teacher != 'null':
                    school.lessons['lessons'][lesson]['name'] = name
                    school.lessons['lessons'][lesson]['teacher'] = teacher
                    school.save()
            elif request.POST.get('new_lesson'):
                lesson = school.lesson_form.copy()
                name = request.POST.get('name')
                teacher = request.POST.get('teacher')
                for i in school.teachers['teachers']:
                    if str(i['ID']) == teacher:
                        teacher = i
                        break
                if name and teacher != 'null':
                    lesson['name'] = name
                    lesson['teacher'] = teacher
                    if len(school.lessons['lessons']) > 0:
                        lesson['ID'] = school.lessons['lessons'][-1]['ID'] + 1
                    else:
                        lesson['ID'] = 0
                    school.lessons['lessons'].append(lesson)
                    school.save()
                    self.range_cycle = school.lessons['lessons']

                
                else:
                    self.error_text = 'Заповніть усі поля'
            elif request.POST.get('id'):
                id = request.POST.get('id')
                return redirect('/school/' + str(id_school) + '/lessons/' + str(id))
        return render(request, self.template_name, 
                    context= {'school': school,
                            'range': self.range_cycle,
                            'error': self.error_text, 'make':make,'select_menu': 5,
                            'teacher_range':teacher_range, 'info_for_edit':info_for_edit,
                            'account':check_account(request,id_school)})
class Info(TemplateView):
    
    def dispatch(self,request,type_info,id_school = None):
        tmp = buttons_menu(request, id_school,aut= False)
        if id_school:
            school = School.objects.get(pk = id_school)
        else:
            school = None
        if tmp != None:
            return redirect(tmp)
        select_info_menu = 0
        if type_info == 'about_us':
            template_name = "MainApp/about_us.html"
            select_info_menu = 1
        elif type_info == 'about_site':
            template_name = "MainApp/about_site.html"
            select_info_menu = 2
        elif type_info == 'contacts':
            template_name = "MainApp/contacts.html"
            select_info_menu = 3
        if request.method == 'POST':
            if request.POST.get("button_info_menu") == '1':
                if id_school:
                    return redirect('/school/' + str(id_school)+ '/info_site/about_us')
                else:
                    return redirect('/info_site/about_us')
            elif request.POST.get("button_info_menu") == '2':
                if id_school:
                    return redirect('/school/' + str(id_school)+ '/info_site/about_site')
                else:
                    return redirect('/info_site/about_site')
            elif request.POST.get("button_info_menu") == '3':
                if id_school:
                    return redirect('/school/' + str(id_school)+ '/info_site/contacts')
                else:
                    return redirect('/info_site/contacts')
        return render(request, template_name, 
                context= {'school': school,
                        'select_menu': 6, 'select_info_menu':select_info_menu,
                        'account':check_account(request,id_school)})
class Clases(TemplateView):
    template_name = "MainApp/clases.html"
    range_cycle = 0
    error_text = None
    def dispatch(self, request, id_school):
        tmp = buttons_menu(request, id_school)
        if tmp != None:
            return redirect(tmp)
        make = False
        school = School.objects.get(pk = id_school)
        teacher_range = school.teachers['teachers']
        if request.user.has_perm('MainApp.show_school'):
            self.range_cycle = school.clases['clases']
        elif request.user.has_perm('MainApp.teacher'):
            self.range_cycle = []
            for i in school.teachers['teachers']:
                if i['login'] == request.user.username:
                    
                    for k in school.clases['clases']:
                        
                        if k['class_teacher']['ID'] == i['ID']:
                            self.range_cycle.append(k)
                    break
        info_for_edit = None
        if request.method == 'POST':
            if request.POST.get('make'):
                make = True
            elif request.POST.get('button_del'):
                 for i in school.clases['clases']:
                    if i['ID'] == int(request.POST.get('button_del')):
                        school.clases['clases'].remove(i)
                        school.save()
                        break
            elif request.POST.get('button_edit'):
                make = True
                for i in school.clases['clases']:
                    if i['ID'] == int(request.POST.get('button_edit')):
                        info_for_edit = i
                        break
            elif request.POST.get('save_school'):
                rank = request.POST.get('rank')
                class_teacher = request.POST.get('teacher')
                name = request.POST.get('name')
                for i in school.teachers['teachers']:
                    if str(i['ID']) == class_teacher:
                        class_teacher = i
                        break
                for i in school.clases['clases']:
                    if i['ID'] == int(request.POST.get('save_school')):
                        clas = school.clases['clases'].index(i)
                        break
                if rank and class_teacher != 'null' and name:
                    school.clases['clases'][clas]['rank'] = rank
                    school.clases['clases'][clas]['class_teacher'] = class_teacher
                    school.clases['clases'][clas]['name'] = name
                    school.save()
            elif request.POST.get('new_class'):
                rank = request.POST.get('rank')
                class_teacher = request.POST.get('teacher')
                name = request.POST.get('name')
                for i in school.teachers['teachers']:
                    if str(i['ID']) == class_teacher:
                        class_teacher = i
                        break
                if rank and class_teacher != 'null' and name:
                    clas = school.class_form.copy()
                    clas['rank'] = rank
                    clas['class_teacher'] = class_teacher
                    clas['name'] = name
                    clas['news_text1'] = 'У цьому блоці ви дізнаетеся останні новини саме вашого класу'
                    clas['news_text2'] = '''Також ви можете запропонувати вашому классному 
                    керівнику розмістита на цьому місці ваш інстаграм. До речі, на випадок якщо бажаючих дуже багато
                            ми додали ось таку прокрутку '''
                    if len(school.clases['clases']) > 0:
                        clas['ID'] = school.clases['clases'][-1]['ID'] + 1
                    else:
                        clas['ID'] = 0
                    school.clases['clases'].append(clas)
                    school.save()
                    self.range_cycle = school.clases['clases']
                else:
                    self.error_text = 'Заповніть усі поля'
            elif request.POST.get('id'):
                id = request.POST.get('id')
                return redirect('/school/' + str(id_school) + '/clases/' + str(id))
        return render(request, self.template_name, 
                    context= {'school': school,
                            'range': self.range_cycle, 'teacher_range':teacher_range,
                            'error': self.error_text, 'make':make,'select_menu': 4, 'info_for_edit':info_for_edit,
                            'account':check_account(request,id_school)})
class Teacher_schadult(TemplateView):
    template_name = "MainApp/schadult_teacher.html"
    def dispatch(self, request, id_school, id_teacher, day):
        days = {
            'Mon': 'Понеділок',
            'Tue': 'Вівторок',
            'Wed': 'Середу',
            'Thr': 'Четвер',
            'Fri': "П'ятницю",
        }
        id_teacher_for_redirect = id_teacher
        school = School.objects.get(pk = id_school)
        tmp = buttons_menu(request, id_school)
        all_lesson_range = school.lessons['lessons'].copy()
        if tmp != None:
            return redirect(tmp)
        for i in range(len(school.teachers['teachers'])):
            if int(school.teachers['teachers'][i]['ID']) == int(id_teacher):
                id_teacher = i
        teacher = school.teachers['teachers'][id_teacher]
        range_schadult = [None,None,None,None,None,None,None,None]
        for i in school.clases['clases']:
            try:
                for j in i['schedult'][day]:
                    if int(j['name']['teacher']['ID']) == id_teacher_for_redirect:
                        range_schadult[i['schedult'][day].index(j)] = {'class':str(i['rank']) + ' - ' + str(i['name']),
                        'name':j['name']['name']}
            except:
                pass
            # if flag:
            #     range_schadult.append({'class':None,'name':None})
        range_days = [{'id':'Mon', 'name':'Понеділок'},
            {'id':'Tue', 'name':'Вівторок'},
            {'id':'Wed', 'name':'Середа'},
            {'id':'Thr', 'name':'Четвер'},
            {'id':'Fri', 'name':"П'ятниця"}]
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id_school) + '/teachers/' + str(id_teacher_for_redirect))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id_school) + '/teachers/' + str(id_teacher_for_redirect) + '/schadult/Mon')
            elif request.POST.get('day_change'):
                return redirect('/school/' + str(id_school) + '/teachers/' + str(id_teacher_for_redirect) + '/schadult/' +request.POST.get('day_change'))
        return render(request, self.template_name, context={ 'menu_class_select':2,
                                                            'select_menu':2,
                                'day':days[day], 'range_schadult':range_schadult, 'range_days':range_days,
                                'day_id': day, 'teacher':teacher, 'account':check_account(request, id_school)
                                })
class Schadult(TemplateView):
    template_name = "MainApp/schadult.html"
    def dispatch(self, request, id_school, id_class, day, edit = False):
        days = {
            'Mon': 'Понеділок',
            'Tue': 'Вівторок',
            'Wed': 'Середу',
            'Thr': 'Четвер',
            'Fri': "П'ятницю",
        }
        edit = bool(edit)
        id_class_for_redirect = id_class
        school = School.objects.get(pk = id_school)
        tmp = buttons_menu(request, id_school)
        all_lesson_range = school.lessons['lessons'].copy()
        if tmp != None:
            return redirect(tmp)
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        clas = school.clases['clases'][id_class]
        lessons_range = clas['lessons_list']
        range_schadult = clas['schedult'][day]
        range_days = [{'id':'Mon', 'name':'Понеділок'},
            {'id':'Tue', 'name':'Вівторок'},
            {'id':'Wed', 'name':'Середа'},
            {'id':'Thr', 'name':'Четвер'},
            {'id':'Fri', 'name':"П'ятниця"}]
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/Mon')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/students/')
            elif request.POST.get('button_menu') == '4':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/lessons/')
            elif request.POST.get('button_menu') == '7':
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/marks/' + "0/type=0")
            elif request.POST.get('day_change'):
                if not edit:
                    return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/' +request.POST.get('day_change'))
                else:
                    return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/' +request.POST.get('day_change') + '/edit/')
            elif request.POST.get('edit_schadult'):
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/' +str(day) + '/edit/')
            elif request.POST.get('save_schadult'):
                
                for j in range(8):
                    if request.POST.get(str(j + 1)) != 'null':
                        if request.POST.get(str(j + 1)) != 'pass':
                            for k in all_lesson_range:
                                print(k)
                                if str(k['ID']) == request.POST.get(str(j + 1)):
                                    flag = True
                                    for clas_check in school.clases['clases']:
                                        try:
                                            if clas_check['schedult'][day][j]['name']:
                                                if str(clas_check['schedult'][day][j]['name']['teacher']['ID']) != str(k['teacher']['ID']):
                                                    flag = True
                                                else:
                                                    flag = False
                                                    break
                                            else:
                                                flag = True
                                            
                                        except:
                                            pass
                                        #     print(-1)
                                        #     temp1 = k
                                    if flag:
                                        temp1 = k
                                    else:
                                        temp1 = ''
                        else:
                            temp1 = ''
                        school.clases['clases'][id_class]["schedult"][day][j] = {'name':temp1, 'num': str(j + 1)}
                school.save()
                return redirect('/school/' + str(id_school) + '/clases/' + str(id_class_for_redirect) + '/schadult/' +str(day))
        return render(request, self.template_name, context={'class':clas, 'menu_class_select':2,
                                                            'select_menu':4,
                                'day':days[day], 'range_schadult':range_schadult, 'range_days':range_days,
                                'day_id': day, 'edit':edit, 'lessons_range': lessons_range, 'account':check_account(request,id_school)
                                })
class Students(TemplateView):
    template_name = "MainApp/students.html"
    range_cycle = 0
    error_text = None
    def dispatch(self, request, id_school):
        
        id_student_for_parents_form = False
        tmp = buttons_menu(request, id_school)
        if tmp != None:
            return redirect(tmp)
        make = False
        info_for_edit = None
        self.range_cycle = []
        school = School.objects.get(pk = id_school)
        teacher_range = school.teachers['teachers']
        range_clases = school.clases['clases']
        if request.user.has_perm('MainApp.show_school'):
            for i in range_clases:
                for j in i['students']:
                    self.range_cycle.append({'student':Student.objects.get(pk = j), 'class': i})
        elif request.user.has_perm('MainApp.teacher'):
            self.range_cycle = []
            for i in school.teachers['teachers']:
                if i['login'] == request.user.username:
                    
                    for k in school.clases['clases']:
                        
                        if k['class_teacher']['ID'] == i['ID']:
                            for stud in k['students']:
                                print(Student.objects.get(pk = stud))
                                self.range_cycle.append({'student':Student.objects.get(pk = stud), 'class': k})
                    break
        if request.method == 'POST':
            print(request.POST.get('button_edit'))
            # print(0)
            if request.POST.get('make'):
                make = 1
            elif request.POST.get('button_del'):
                student = Student.objects.get(pk = request.POST.get('button_del'))
                user = User.objects.get(username = student.login)
                for i in school.clases['clases']:
                    if student.id in i['students']:
                        i['students'].remove(student.id)
                        student.delete()
                        user.delete()
                        school.save()
                        return redirect('/school/' + str(school.id) + '/students/')

                
            elif request.POST.get('button_edit'):
                
                make = 1
                info_for_edit = Student.objects.get(pk = request.POST.get('button_edit'))
            elif request.POST.get('new_student'):
                student = Student.objects.get(pk = int(request.POST.get('student_id')))
                student.name_parrent1 = request.POST.get('name_parrent1')
                student.number_phone_parrent1 = request.POST.get('number_phone_parrent1')
                student.work_parrent1 = request.POST.get('work_parrent1')
                student.name_parrent2 = request.POST.get('name_parrent2')
                student.number_phone_parrent2 = request.POST.get('number_phone_parrent2')
                student.work_parrent2 = request.POST.get('work_parrent2')
                student.save()
            elif request.POST.get('save_student'):
                student = Student.objects.get(pk = request.POST.get('save_student'))
                student.name = request.POST.get('name')
                student.surname = request.POST.get('surname')
                student.second_name = request.POST.get('second_name')
                user = User.objects.get(username = student.login)
                student.login = request.POST.get('email')
                student.email = request.POST.get('email')
                
                student.number_phone = request.POST.get('number_phone')
                student.adress = request.POST.get('adress')
                if student.name and student.surname and student.second_name and student.birthday and student.age and student.login and student.email and student.number_phone and student.adress:
                    student.save()
                    user.username = student.login 
                    user.save()
                    make = 2
                    info_for_edit = student 
                else:
                    make = 1
                    info_for_edit = student 
            elif request.POST.get('save_student1'):
                student = Student.objects.get(pk = int(request.POST.get('save_student1')))
                student.name_parrent1 = request.POST.get('name_parrent1')
                student.number_phone_parrent1 = request.POST.get('number_phone_parrent1')
                student.work_parrent1 = request.POST.get('work_parrent1')
                student.name_parrent2 = request.POST.get('name_parrent2')
                student.number_phone_parrent2 = request.POST.get('number_phone_parrent2')
                student.work_parrent2 = request.POST.get('work_parrent2')
                student.save()
            elif request.POST.get('next1'):
                
                try:
                # print(1)
                    if request.POST.get("birthday") and request.POST.get('class_stud'):
                        # print(2)
                        Student.objects.create(
                            name = request.POST.get('name'),
                            surname = request.POST.get('surname'),
                            second_name = request.POST.get('second_name'),
                            birthday = request.POST.get('birthday'),
                            age = str(calculate_age(datetime.strptime(request.POST.get('birthday'), "%Y-%m-%d"))),
                            login = request.POST.get('email'),
                            marks = {
                                0:[],
                                1:[],
                                2:[],
                                3:[],
                                4:[],
                                5:[],
                                6:[],
                                7:[],
                                8:[],
                            },
                            password = str(randint(10000000,99999999)),
                            email = request.POST.get('email'),
                            number_phone = request.POST.get('number_phone'),
                            adress = request.POST.get('adress'),
                            name_parrent1 = '',
                            number_phone_parrent1 = '',
                            work_parrent1 = '',
                            name_parrent2 = '',
                            number_phone_parrent2 = '',
                            work_parrent2 = ''
                        )
                        
                        for clas_num in school.clases['clases']:
                            # print(clas_num['ID'], request.POST.get('class_stud'))
                            if str(clas_num['ID']) == request.POST.get('class_stud'):
                                id_class = school.clases['clases'].index(clas_num)
                        temp = school.clases['clases'][id_class].keys()
                        temp1 = len(Student.objects.all())
                        student = Student.objects.all()[temp1 - 1]
                        temp_list = []
                        marks_temp = []
                        for el in range(30):
                            marks_temp.append({'ID': el,"mark": ' '})
                        for j in school.clases['clases'][id_class]['lessons_list']:
                            temp_list.append({'ID':j['ID'],'marks':marks_temp})
                        for i in student.marks.keys():
                            student.marks[i] = temp_list
                        student.save()
                        id_student_for_parents_form = str(Student.objects.all()[len(Student.objects.all()) - 1].id)
                        # print(id_student_for_parents_form)
                        if 'students' in temp:
                            school.clases['clases'][id_class]['students'].append(Student.objects.all()[temp1-1].id)
                        else:
                            school.clases['clases'][id_class]['students'] = [Student.objects.all()[temp1-1].id]
                        # print(3)
                        school.save()
                        user = User.objects.create_user(
                            username=student.login,
                            email=student.email,
                            password=student.password
                        )
                        permission = Permission.objects.get(codename='view_student')
                        user.user_permissions.add(permission)
                        user.save()
                        make = 2
                    else:
                        make = 1
                        self.error_text = 'Заповніть усі поля'
                except:
                    make = 1
                    self.error_text = 'Заповніть усі поля'
            elif request.POST.get('id'):
                
                id = request.POST.get('id')
                return redirect('/school/' + str(id_school) + '/students/' + str(id))
        return render(request, self.template_name, 
                    context= {'school': school,
                            'range': self.range_cycle, 'teacher_range':teacher_range,
                            'error': self.error_text, 'make':make,'select_menu': 3,
                            'clases':range_clases,
                            'id_student_for_parents_form':id_student_for_parents_form,
                            'account':check_account(request,id_school),
                            'info_for_edit':info_for_edit})
class School_info(TemplateView):
    template_name = "MainApp/school_info.html"

    def dispatch(self, request, id):
        tmp = buttons_menu(request, id)
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id)
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id) + '/info')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id) + '/contacts')
        return render(request, self.template_name, 
                context= {'school': school,
                            'select_menu':1, 'menu_school_select':2,'account':check_account(request, id)})
class School_contacts(TemplateView):
    template_name = "MainApp/school_contacts.html"

    def dispatch(self, request, id):
        tmp = buttons_menu(request, id)
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id)
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id) + '/info')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id) + '/contacts')
        return render(request, self.template_name, 
                context= {'school': school,
                            'select_menu':1, 'menu_school_select':3,'account':check_account(request,id)})

class Show_school(TemplateView):
    
    template_name = "MainApp/school.html"
    
    
    type_page = ''
    range_cycle = 0
    error_text = None
    
    def dispatch(self, request, id):
        tmp = buttons_menu(request, id)
        if tmp != None:
            return redirect(tmp)
        school = School.objects.get(pk = id)
        if request.method == 'POST':
            if request.POST.get('button_menu') == '1':
                return redirect('/school/' + str(id))
            elif request.POST.get('button_menu') == '2':
                return redirect('/school/' + str(id) + '/info')
            elif request.POST.get('button_menu') == '3':
                return redirect('/school/' + str(id) + '/contacts')
        return render(request, self.template_name, 
                    context= {'school': school,
                                'select_menu':1, 'menu_school_select':1, 'account':check_account(request, id)})

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






        