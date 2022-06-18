from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import*
from datetime import datetime, date
from random import randint
# from DjangoProject import urls

# Create your views here.
# print(urls.urlpatterns)
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
def home(request):
    return render(request, 'MainApp/home.html')
def info(request):
    return render(request,'MainApp/info.html')
class Edit_info(TemplateView):
    template_name = "MainApp/editinfo.html"
    error_text = None
    def dispatch(self,request,id,id_class):
        for i in range(len(School.objects.all())):
            if School.objects.all()[i].id == id:
                id = i
        school = School.objects.all()[id]
        for i in school.clases['clases']:
            if int(i['ID']) == int(id_class):
                clas = i
                id_class = school.clases['clases'].index(i)
        teachers = school.teachers['teachers']
        if request.method == 'POST':
            name = request.POST.get('name')
            class_teacher = request.POST.get('teacher')
            rank = request.POST.get('rank')
            if name and rank:
                if class_teacher != 'null':
                    for i in school.teachers['teachers']:
                        if i['ID'] == int(class_teacher):
                            class_teacher = i
                            break
                    school.clases['clases'][id_class]['class_teacher'] = class_teacher
                school.clases['clases'][id_class]['name'] = name
                
                school.clases['clases'][id_class]['rank'] = rank
                school.save()
                return redirect('/school/' + str(school.id) + '/' + str(clas['ID']))
            else:
                self.error_text = 'Заповніть усі поля'
            
        return render(request, self.template_name, context={'class':clas, 'teacher_range':teachers,
                    'error':self.error_text})
class Show_student_marks(TemplateView):
    template_name = "MainApp/marks.html"
    def dispatch(self, request, id,id_class, id_student):
        school = School.objects.get(pk = id)
        for i in school.clases['clases']:
            if int(i['ID']) == int(id_class):
                clas = i
        student = Student.objects.get(pk = id_student)
        range1 = student.marks
        range2 = []
        for i in range(30):
            range2.append(' ')
        return render(request, self.template_name, context={'range': range1,
                    'range2': range(30), 'student':student, 'class':clas})
class Show_lesson_marks(TemplateView):
    template_name = "MainApp/marks.html"
    def dispatch(self, request, id, id_lesson, id_class):
        school = School.objects.get(pk = id)
        for i in school.clases['clases']:
            if int(i['ID']) == int(id_class):
                clas = i
        for i in school.lessons['lessons']:
            if i['ID'] == id_lesson:
                lesson = i
                break
        for i in school.teachers['teachers']:
            if i['ID'] == lesson['teacher']['ID']:
                teacher = i
                break
        
        range1 = []
        for i in clas['students']:
            range1.append(Student.objects.get(pk = i))
        return render(request, self.template_name, context={'range': range1,
                    'range2': range(30), 'class':clas, 'lesson':lesson})
class Schoolswork(TemplateView):
    template_name = "MainApp/schools.html"
    id = -1
    def dispatch(self, request):
        
        if request.method == "POST":
            if request.POST.get('del'):
                school = School.objects.get(pk = request.POST.get('del'))
                school.delete()
            else:
                self.id = request.POST.get('id')
                return redirect('/school/' + str(self.id))
            # return redirect("school")
        # print(people[0].title
        school = School.objects.all()
    # print(len(school), '--------------------------------------')
        return render(request, self.template_name, context= {"school": school, 'range': school})
class Show_class(TemplateView):
    template_name = "MainApp/class.html"
    def dispatch(self,request,id,id_class):
        for i in range(len(School.objects.all())):
            if School.objects.all()[i].id == id:
                id = i
        school = School.objects.all()[id]
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        clas = school.clases['clases'][id_class]
        lesson_range = clas['lessons_list']
        student_range = []
        student = 0
        students = Student.objects.all()
        for i in students:
            if i.id in clas['students']:
                student_range.append(i)
        if request.method == 'POST':
            if request.POST.get('but_id') == 'edit_lessons':
                return redirect('/school/' + str(school.id) + '/' + str(clas['ID']) + '/lessons')
            elif request.POST.get('but_id') == 'edit_schadult':
                return redirect('/school/' + str(school.id) + '/' + str(clas['ID']) + '/schadult')
            elif request.POST.get('but_id') == 'edit_info':
                return redirect('/school/' + str(school.id) + '/' + str(clas['ID']) + '/info')
            elif request.POST.get('but_id') == 'edit_student':
                return redirect('/school/' + str(school.id) + '/' + str(clas['ID']) + '/makestudent')
            elif request.POST.get('but_id') == 'show_student':
                temp = request.POST.get('students')
                if temp != '' and temp != None:
                    student = Student.objects.get(pk = temp)
                    self.student_last = student
            elif request.POST.get('but_id') == 'show_lesson':
                temp = request.POST.get('lessons')
                if temp != '' and temp != None:
                    return redirect('/school/' + str(school.id) + '/lesson/' + str(temp) + '/' + str(clas['ID']))
            if request.POST.get('but_id') == 'open_student':
                return redirect('/school/' + str(school.id) + '/' + str(clas['ID']) + '/' + str(self.student_last.id) + '/marks')
        return render(request, self.template_name, context={'class':clas, 
                                'lesson_range': lesson_range, 'student_range': student_range,
                                'student': student
                                })
class Teacher_page(TemplateView):
    template_name = "MainApp/teacher.html"
    def dispatch(self, request, id, id_teacher):
        school = School.objects.get(pk = id)
        for i in school.teachers['teachers']:
            if i['ID'] == id_teacher:
                teacher = i
                break
        lessons = []
        for i in school.lessons['lessons']:
            if i['teacher']['ID'] == id_teacher:
                lessons.append(i)

        if request.method == 'POST':
            if request.POST.get('but') != None:
                return redirect('/school/' + str(id) + '/lesson/' + request.POST.get('but'))
        return render(request, self.template_name, context = {'lessons':lessons,
                        'teacher': teacher})
class Teacher_class_page(TemplateView):
    template_name = "MainApp/teacher_class.html"
    def dispatch(self, request, id, id_lesson):
        school = School.objects.get(pk = id)
        for k in school.lessons['lessons']:
            if k['ID'] == id_lesson:
                lesson = k
                break
        for i in school.teachers['teachers']:
            if i['ID'] == lesson['teacher']['ID']:
                teacher = i
                break
        clases = []
        for i in school.clases['clases']:
            for j in i['lessons_list']:
                if id_lesson == j['ID']:
                    clases.append(i)
        # print(clases)
        if request.method == 'POST':
            if request.POST.get('but') != None:
                return redirect('/school/' + str(id) + '/lesson/' + str(id_lesson)  + '/' + request.POST.get('but'))
        return render(request, self.template_name, context = {'classes':clases,
                        'teacher': teacher, 'lesson':lesson})
class Auth(TemplateView):
    template_name = "MainApp/auth.html"
    type_page = 'start'
    def dispatch(self, request, type_page = None):
        error_text = 0
        if type_page != None:
            self.type_page = str(type_page)
        if request.method == 'POST':
            if request.POST.get('button_choise') != None:
                return redirect('/auth/' + request.POST.get('button_choise'))
            if request.POST.get('submit') == 'teacher':
                school = School.objects.get(pk = int(request.POST.get('school_name')))
                for i in school.teachers['teachers']:
                    if i['login'] == request.POST.get('login'):
                        if i['password'] == request.POST.get('password'):
                            print(1)
        return render(request, self.template_name, context ={
            'type_page':self.type_page, 'school_range':School.objects.all(),
            'error_text':error_text
        })
class Make_student(TemplateView):
    template_name = "MainApp/makestudent.html"
    error_text = None
    def dispatch(self,request,id,id_class):
        for i in range(len(School.objects.all())):
            if School.objects.all()[i].id == id:
                id = i
        school = School.objects.all()[id]
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        clas = school.clases['clases'][id_class]

        if request.method == 'POST':

            try:
                if request.POST.get("birthday"):
                    Student.objects.create(
                        name = request.POST.get('name'),
                        surname = request.POST.get('surname'),
                        second_name = request.POST.get('second_name'),
                        birthday = request.POST.get('birthday'),
                        age = str(calculate_age(datetime.strptime(request.POST.get('birthday'), "%Y-%m-%d"))),
                        login = request.POST.get('email'),
                        marks = {},
                        password = str(randint(10000000,99999999)),
                        email = request.POST.get('email'),
                        number_phone = request.POST.get('number_phone'),
                        adress = request.POST.get('adress'),
                        name_parrent1 = request.POST.get('name_parrent1'),
                        number_phone_parrent1 = request.POST.get('number_phone_parrent1'),
                        work_parrent1 = request.POST.get('work_parrent1'),
                        name_parrent2 = request.POST.get('name_parrent2'),
                        number_phone_parrent2 = request.POST.get('number_phone_parrent2'),
                        work_parrent2 = request.POST.get('work_parrent2')
                    )
                    temp = school.clases['clases'][id_class].keys()
                    temp1 = len(Student.objects.all())
                    if 'students' in temp:
                        school.clases['clases'][id_class]['students'].append(Student.objects.all()[temp1-1].id)
                    else:
                        school.clases['clases'][id_class]['students'] = [Student.objects.all()[temp1-1].id]
                    school.save()
                    return redirect('/school/' + str(school.id) + '/' + str(clas['ID']))
                else:
                    self.error_text = 'Заповніть усі поля'
            except:
                self.error_text = 'Заповніть усі поля'
            
        return render(request, self.template_name, context = {'error': self.error_text})
class Edit_lessons(TemplateView):
    template_name = "MainApp/editlessons.html"
    
    def dispatch(self,request,id,id_class):
        for i in range(len(School.objects.all())):
            if School.objects.all()[i].id == id:
                id = i
        school = School.objects.all()[id]
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        clas = school.clases['clases'][id_class]
        lesson_range = clas['lessons_list']
        all_lesson_range = school.lessons['lessons'].copy()
        ids = []
        for i in range(len(all_lesson_range)):
            if all_lesson_range[i] in lesson_range:
                ids.append(i)
        ids = ids[::-1]
        # print(ids)
        for i in ids:
            del all_lesson_range[i]
        # print(all_lesson_range)
        if request.method == 'POST':
            if request.POST.get('button') == '2':
                # print(3)
                if request.POST.get('unselected') != None:
                    id = request.POST.get('unselected')
                    for i in all_lesson_range:
                        # print(2)
                        if str(i['ID']) == id and i not in school.clases['clases'][id_class]['lessons_list']:
                            # print(1)
                            school.clases['clases'][id_class]['lessons_list'].append(i)
                            school.save()
                            for stud in Student.objects.all():
                                if stud.id in school.clases['clases'][id_class]['students']:
                                    name = i['name']
                                    stud.marks[name] = []
                                    stud.save() 
                            del all_lesson_range[all_lesson_range.index(i)]
            if request.POST.get('button') == '1':
                if request.POST.get('selected') != None:
                    id = request.POST.get('selected')
                    for i in lesson_range:
                        # print(2)
                        if str(i['ID']) == id and i not in all_lesson_range:
                            print(1)
                            school.clases['clases'][id_class]['lessons_list'].remove(i)
                            school.save()
                            all_lesson_range.append(i)
                            for stud in Student.objects.all():
                                if stud.id in school.clases['clases'][id_class]['students']:
                                    name = i['name']
                                    del stud.marks[name]
                                    stud.save() 
            if request.POST.get('button') == '3':
                return redirect('/school/' + str(school.id) + '/' + str(clas['ID']))
        return render(request, self.template_name, context={'class':clas, 
                                'lesson_range': lesson_range,
                                'all_lesson_range':all_lesson_range})
class Edit_schadult(TemplateView):
    template_name = "MainApp/editschadult.html"
    def dispatch(self, request, id, id_class):
        for i in range(len(School.objects.all())):
            if School.objects.all()[i].id == id:
                id = i
        school = School.objects.all()[id]
        for i in range(len(school.clases['clases'])):
            if int(school.clases['clases'][i]['ID']) == int(id_class):
                id_class = i
        clas = school.clases['clases'][id_class]
        lesson_range = []
        lesson_range_for_html = clas['lessons_list']
        all_lesson_range = school.lessons['lessons'].copy()
        range_week = clas['schedult'].keys()
        for i in range_week:
            temp = {'lessons': clas['schedult'][i], 'day': i}
            lesson_range.append(temp)
        # print(lesson_range)
        if request.method == 'POST':
            for i in range_week:
                for j in range(8):
                    # print(str(j + 1) + '-' + i)
                    print(request.POST.get(str(j + 1) + '-' + i))
                    if request.POST.get(str(j + 1) + '-' + i) != 'null':
                        print(1)
                        if request.POST.get(str(j + 1) + '-' + i) != 'pass':
                            for k in all_lesson_range:
                                # print(k['ID'])
                                if str(k['ID']) == request.POST.get(str(j + 1) + '-' + i):
                                    temp1 = k['name'] + ' (' + k['teacher']['name'] + ')' 
                        else:
                            temp1 = ''
                        school.clases['clases'][id_class]["schedult"][i][j] = {'name':temp1, 'num': str(j + 1)}
            school.save()
            return redirect('/school/' + str(school.id) + '/' + str(clas['ID']))
        return render(request, self.template_name, 
                    context= {'school': school, 'class': clas, 
                            'lesson_range': lesson_range, 
                            "all_lesson_range": lesson_range_for_html})

class Show_school(TemplateView):
    
    template_name = "MainApp/school.html"
    
    
    type_page = ''
    range_cycle = 0
    error_text = None
    
    def dispatch(self, request, id):
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
        school = School.objects.get(pk = id)
        teacher_range = school.teachers['teachers']
        if request.method == 'POST':
            if request.POST.get("id") == '1':
                self.type_page = 'create_class'
            elif request.POST.get("id") == '2':
                self.type_page = 'create_lesson'
            # print(request.POST.get("id"))
            # print(type_page)
            elif request.POST.get("id") == "4" :

                rank = request.POST.get('rank')
                class_teacher = request.POST.get('class_teacher')
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

                    if len(school.clases['clases']) > 0:
                        clas['ID'] = school.clases['clases'][-1]['ID'] + 1
                    else:
                        clas['ID'] = 0
                    school.clases['clases'].append(clas)
                    school.save()
                    self.type_page = 'show_clases'
                    self.range_cycle = school.clases['clases']
                else:
                    self.type_page = 'create_class'
                    self.error_text = 'Заповніть усі поля'
            elif request.POST.get('id') == '3':
                self.type_page = 'show_clases'
                self.range_cycle = school.clases['clases']
            elif request.POST.get('id') == '5':
                lesson = school.lesson_form.copy()
                name = request.POST.get('lesson_name')
                teacher = request.POST.get('teacher_name_lesson')
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
                    self.type_page = 'show_lessons'
                    self.range_cycle = school.lessons['lessons']
                else:
                    self.type_page = 'create_lesson'
                    self.error_text = 'Заповніть усі поля'
            elif request.POST.get('id') == '6':
                self.type_page = 'show_lessons'
                self.range_cycle = school.lessons['lessons']
            elif request.POST.get("id_class") != None:
                return redirect('/school/' + str(school.id) + '/' + str(request.POST.get("id_class")))
            elif request.POST.get('id') == '7':
                self.type_page = 'create_teacher'
            elif request.POST.get('id') == '8':
                name = request.POST.get('teacher_name')
                login = request.POST.get('teacher_login')
                password = request.POST.get('teacher_password')
                teacher = {}
                teacher['name'] = name
                teacher['login'] = login
                teacher['password'] = password
                if name and login and password:
                    if len(school.teachers['teachers']) > 0:
                        teacher['ID'] = school.teachers['teachers'][-1]['ID'] + 1
                    else:
                        teacher['ID'] = 0
                    school.teachers['teachers'].append(teacher)
                    school.save()
                    self.type_page = 'show_teachers'
                    self.range_cycle = school.teachers['teachers']
                else:
                    self.type_page = 'create_teacher'
                    self.error_text = 'Заповніть усі поля'
            elif request.POST.get('id') == '10':
                self.type_page = 'show_teachers'
                self.range_cycle = school.teachers['teachers']
            elif request.POST.get('button_lesson') != None:
                
                return redirect('/school/' + str(id) + '/lesson/'  + request.POST.get('button_lesson'))
            elif request.POST.get('button_teacher') != None:
                return redirect('/school/' + str(school.id) + '/teacher/' + str(request.POST.get('button_teacher')))
            elif request.POST.get('del_class') != None:
                for i in school.clases['clases']:
                    if i['ID'] == int(request.POST.get('del_class')):
                        school.clases['clases'].remove(i)
                        school.save()
                        self.type_page = 'show_clases'
                        self.range_cycle = school.clases['clases']
            elif request.POST.get('del_lesson') != None:
                for i in school.lessons['lessons']:
                    if i['ID'] == int(request.POST.get('del_lesson')):
                        school.lessons['lessons'].remove(i)
                        school.save()
                        self.type_page = 'show_lessons'
                        self.range_cycle = school.lessons['lessons']
            elif request.POST.get('del_teacher') != None:
                for i in school.teachers['teachers']:
                    if i['ID'] == int(request.POST.get('del_teacher')):
                        school.teachers['teachers'].remove(i)
                        school.save()
                        self.type_page = 'show_teachers'
                        self.range_cycle = school.teachers['teachers']
            return render(request, self.template_name, 
                        context= {'school': school, 'type': self.type_page, 
                                'range': self.range_cycle, 'teacher_range':teacher_range,
                                'error': self.error_text})

        return render(request, self.template_name, 
                    context= {'school': school, 'type': self.type_page, 
                            'range': self.range_cycle, 'teacher_range':teacher_range,
                            'error': self.error_text})
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
            if school.title and school.number and school.town and school.password:
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