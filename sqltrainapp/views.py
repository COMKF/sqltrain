import json
from .models import User, Question, Doques
from django.db import connection
import operator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .form import register_f, login_f, changepwd_f
from django.urls import reverse


def check(func):  # 使用装饰器验证用户登录
    def wrapper(*args, **kw):
        x = args[0]  # 先获取request
        if x.session.get('user_name'):  # 进行验证，用户是否登录
            # request.session.get('user_name')和request.session['user_name']，两者都可以取出session中name的值
            # 但是如果session中不存在name的值， 前者返回None，可进行判断。后者直接抛出异常。
            # 使用request.session['user_name']的效代码如下：
            # try:
            #     request.session['user_name']
            # except KeyError:
            #     return render(request, 'sqltrainapp/login.html')
            return func(*args, **kw)  # 如果登录，则执行原函数
        else:
            return render(x, 'sqltrainapp/index.html')  # 如果没有登录，则跳转到index页面

    return wrapper


def check_type_1(func):  # 使用装饰器验证用户权限
    def wrapper(*args, **kw):
        x = args[0]  # 先获取request
        if x.session.get('user_name'):  # 进行验证，用户是否登录
            if User.objects.get(user_name=x.session.get('user_name')).user_type == '1':  # 验证用户权限
                return func(*args, **kw)  # 如果登录，则执行原函数
        else:
            return render(x, 'sqltrainapp/index.html')  # 如果没有登录，则跳转到index页面

    return wrapper


def check_type_2(func):
    def wrapper(*args, **kw):
        x = args[0]  # 先获取request
        if x.session.get('user_name'):  # 进行验证，用户是否登录
            if User.objects.get(user_name=x.session.get('user_name')).user_type == '2':  # 验证用户权限
                return func(*args, **kw)  # 如果登录，则执行原函数
        else:
            return render(x, 'sqltrainapp/index.html')  # 如果没有登录，则跳转到index页面

    return wrapper


def check_type_3(func):
    def wrapper(*args, **kw):
        x = args[0]  # 先获取request
        if x.session.get('user_name'):  # 进行验证，用户是否登录
            if User.objects.get(user_name=x.session.get('user_name')).user_type == '3':  # 验证用户权限
                return func(*args, **kw)  # 如果登录，则执行原函数
        else:
            return render(x, 'sqltrainapp/index.html')  # 如果没有登录，则跳转到index页面

    return wrapper


# @check
def login(request):
    print('[Info    ] you are login')
    return render(request, 'sqltrainapp/login.html')


def login_detail(request):
    if request.method == 'POST':
        # Django获取表单中值的方法
        r = request.POST
        f = login_f(r)
        if f.is_valid():
            request.session['user_name'] = f.cleaned_data.get('user_name')  # 把用户名放入session中
            return render(request, 'sqltrainapp/index.html')
        else:
            return render(request, 'sqltrainapp/login.html', {"error": f.errors})
    else:
        if request.session.get('user_name'):
            return render(request, 'sqltrainapp/index.html')
        else:
            return render(request, 'sqltrainapp/login.html')


def register(request):
    return render(request, 'sqltrainapp/register.html')


def register_detail(request):
    if request.method == "POST":  # 这里POST一定要大写，验证request的方法
        # 获取请求内容，做验证
        r = request.POST
        f = register_f(r)  # request.POST：将接收到的数据通过Form1验证
        user_name = r['user_name']
        cls = r['cls']

        if f.is_valid():  # 验证请求的内容和Form里面的是否验证通过。通过是True，否则False。
            id = int(User.objects.raw('Select user_id,max(user_id) from sqltrainapp_user')[0].user_id) + 1
            u = User(user_id='%05d' % id, user_name=f.cleaned_data['user_name'], pwd=f.cleaned_data['pwd'], user_type=3,
                     school=r['school'], faculties=r['faculties'], cls=r['cls'])

            # print("123123123",f.cleaned_data['user_name'])  # cleaned_data类型是字典，里面是提交成功后的信息。
            u.save()
            return render(request, 'sqltrainapp/login.html', {"msg": '注册成功，请登录'})
        else:  # 错误信息包含是否为空，或者符合正则表达式的规则
            print(type(f.errors), f.errors)  # errors类型是ErrorDict，里面是ul，li标签
            return render(request, "sqltrainapp/register.html",
                          {"error": f.errors, 'f': f, "user_name": user_name, "cls": cls})
    else:
        return render(request, "sqltrainapp/register.html")


# @check
def logout(request):
    try:
        del request.session['user_name']
    except KeyError:
        pass
    return render(request, 'sqltrainapp/login.html', {"msg": '已注销'})


def index(request):
    return render(request, 'sqltrainapp/index.html')


# @check
def Getting_Started(request):
    return render(request, 'sqltrainapp/Getting_Started.html')


# @check
def basic(request):
    return render(request, 'sqltrainapp/questions/basic.html')


@check
def basicall(request, question_id):
    question = Question.objects.get(ques_id=question_id)
    # question = Question.objects.all()
    qid = question.ques_id
    question_content = question.ques_content
    sql = question.answer
    print("[Info    ]" + sql)
    print('[Info    ]' + str(qid))
    # members = Question.objects.raw("SELECT * FROM sqltrainapp_question")    # [:] 注释这里就会从set变成list
    # 返回的默认是list
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqltrainapp_question")
    members = cursor.fetchall()
    print('[Info    ]' + str(type(members)))  # <class 'django.db.models.query.RawQuerySet'>
    # print('[Info    ]' + str(members))
    # l = len(members)
    for x in members:
        print('[Info    ]' + str(x))
    return render(request, 'sqltrainapp/questions/basic/selectall.html', {
        'members': members,
        'question_content': question_content,
        'sql_raw': sql,
        'qid': qid
    })


# 运行用户提供的sql语句，将运行结果与参考答案的结果进行比较
def result(request):
    # django的SCUD可以跳过模型层，直接执行自定义的SQL
    # 通过param和占位符，可以防止SQL注入攻击
    # 如果sql语句中包含%，比如'38%'，要使用'38%%' 来正确的传递参数
    print('[Info    ]you arrive result')
    data1 = request.GET.get('a')  # 可以通过request获取post的form的id对应的数据
    data2 = request.GET.get('b')
    data3 = request.GET.get('c')
    print('[Info    ]' + str(data1))  # 用户输入的sql
    print('[Info    ]' + str(data2))  # 参考答案的sql
    print('[Info    ]' + str(data3))
    results = "OOPS! there has nothing"
    if data1:
        # 本来想传递members，但是不会用js传递这个members，这里传sql_raw，
        # results = Members.objects.raw(data1)
        cursor1 = connection.cursor()
        # cursor1.execute(data2)
        cursor1.execute("select * from sqltrainapp_question")
        row1 = cursor1.fetchall()
        print('[Info    ]' + str(type(row1)))
        print('[Info    ]' + 'length: ' + str(len(row1)))
        for x in row1:
            print(x)

        # 这里的结果是列表，而不是字段，所以是不带字段名称的, 当然也可以处理成key：value的形式
        # 对用户输入的sql语句进行查询
        cursor = connection.cursor()
        cursor.execute(data1)
        row = cursor.fetchall()
        print('[Info    ]' + str(type(row)))
        print('[Info    ]' + 'length: ' + str(len(row)))
        for x in row:
            print(x)

        # 对两个结果进行比较，list之间的比较，如果相同就返回true，否则返回false
        # false时在进一步比较哪里不同，给出不同的地方
        cmpresult = operator.eq(row1, row)
        if cmpresult == False:
            pass
        print('[Info    ]' + str(cmpresult))
        # 对set进行比较，
        # 先比较长度
        # 再进行交集运算找出相同的set集合，然后就可以找出不同的地方

        # 给出错误原因，提示信息，放入cmpresult，并写入数据库，需要传过来用户的id，问题的id，
        # 写入 错误原因 及 用户的答案
        uname = request.session.get('user_name')
        print('[Info    ]' + str(uname))
        # if uname :
        #     user = User.objects.get(user_name=uname)
        #     uid = user.user_id
        #     qid = data3
        #     answ = data1
        #     result=cmpresult
        #     d = Doques(someone=uid, someques=qid, answ_content=answ, result_type=result)
        #     d.save()

        # 返回查询结果和提示信息
        ret = {'result': row,
               'cmpresult': cmpresult
               }
        return HttpResponse(json.dumps(ret), content_type='application/json')
        # return HttpResponse(ret)

    else:
        print('[Info    ]Ok , you must enter sql')
        ret = 'you must enter sqlstring'
        return HttpResponse(ret)

    print('[Info    ]' + str(type(results)))
    for x in results:
        print(x)
        # print(x.surname)
    # 到这里就得到了用户输入sql语句的结果
    # 下面进行判断set<>是否相同，a,b  a-b
    ret = results
    return HttpResponse(ret)
    # return render(request, 'train/result.html', {'results': results})


# @check
def joins(request):
    return render(request, 'sqltrainapp/questions/joins.html')


# @check
def aggregates(request):
    return render(request, 'sqltrainapp/questions/aggregates.html')


# @check
def date(request):
    return render(request, 'sqltrainapp/questions/date.html')


# @check
def string(request):
    return render(request, 'sqltrainapp/questions/string.html')


# @check
def recursive(request):
    return render(request, 'sqltrainapp/questions/recursive.html')


# @check
def about(request):
    return render(request, 'sqltrainapp/about.html')


# @check
def options(request):
    return render(request, 'sqltrainapp/options.html')


# @check
def moban(request):
    return render(request, 'sqltrainapp/moban.html')


def personinfo(request, user_name):
    if User.objects.filter(user_name=user_name):
        user = User.objects.filter(user_name=user_name)[0]
        if user_name == request.session.get('user_name'):
            return render(request, 'sqltrainapp/personinfo/personinfo.html', {"user": user})
            # if u.user_type == '1':
            #     # return render(request, 'sqltrainapp/personinfo/test.html')
            #     return render(request, 'sqltrainapp/personinfo/admin.html')
            # elif u.user_type == '2':
            #     return render(request, 'sqltrainapp/personinfo/teacher.html')
            # elif u.user_type == '3':
            #     return render(request, 'sqltrainapp/personinfo/student.html')
        else:
            return render(request, 'sqltrainapp/personinfo/OtherPersonInfo.html', {"user": user})
    else:
        return HttpResponse("%s 用户不存在." % user_name)


@check
def changeinfo(request):
    if request.method == "POST":
        user_name = request.session.get('user_name')
        user = User.objects.get(user_name=user_name)
        r = request.POST
        user.school = r['school']
        user.faculties = r['faculties']
        user.cls = r['cls']
        user.save()
        return HttpResponseRedirect(reverse('sqltrainapp:personinfo', args=(user_name,)))


@check
def changepwd(request):
    user_name = request.session.get('user_name')
    user = User.objects.get(user_name=user_name)
    return render(request, 'sqltrainapp/personinfo/changepwd.html', {"user": user})


@check
def changepwd_detail(request):
    if request.method == "POST":
        r = request.POST
        user_name = request.session.get('user_name')
        user = User.objects.get(user_name=user_name)
        f = changepwd_f(r, user_name)  # request.POST：将接收到的数据通过Form1验证

        if f.is_valid():  # 验证请求的内容和Form里面的是否验证通过。通过是True，否则False。
            user.pwd = f.cleaned_data['pwd']
            user.save()
            return render(request, 'sqltrainapp/personinfo/changepwd.html', {"msg": '密码修改成功', "user": user})
        else:  # 错误信息包含是否为空，或者符合正则表达式的规则
            print(type(f.errors), f.errors)  # errors类型是ErrorDict，里面是ul，li标签
            return render(request, 'sqltrainapp/personinfo/changepwd.html',
                          {"error": f.errors, "user": user})


@check_type_1
def A_manage_T(request):
    user = User.objects.get(user_name=request.session.get('user_name'))
    list = User.objects.filter(user_type='2')
    return render(request, 'sqltrainapp/personinfo/A_manage_T.html', {'list': list, 'user': user})


@check_type_1
def revoke_T(request, user_id):
    user = User.objects.get(user_id=user_id)
    user.user_type = '3'
    user.save()
    return HttpResponseRedirect(reverse('sqltrainapp:A_manage_T'))


@check_type_1
def A_manage_S(request):
    user = User.objects.get(user_name=request.session.get('user_name'))
    list = User.objects.filter(user_type='3')
    return render(request, 'sqltrainapp/personinfo/A_manage_S.html', {'list': list, 'user': user})


@check_type_1
def promote_S(request, user_id):
    user = User.objects.get(user_id=user_id)
    user.user_type = '2'
    user.save()
    return HttpResponseRedirect(reverse('sqltrainapp:A_manage_S'))


@check_type_1
def delete(request, user_id):
    user = User.objects.get(user_id=user_id)
    if user.user_type == '2':
        user.delete()
        return HttpResponseRedirect(reverse('sqltrainapp:A_manage_T'))
    if user.user_type == '3':
        user.delete()
        return HttpResponseRedirect(reverse('sqltrainapp:A_manage_S'))


@check_type_2
def T_show_S(request):
    user = User.objects.get(user_name=request.session.get('user_name'))
    list = User.objects.filter(user_type='3')
    return render(request, 'sqltrainapp/personinfo/T_show_S.html', {'list': list, 'user': user})


@check_type_2
def T_show_Q(request):
    user = User.objects.get(user_name=request.session.get('user_name'))
    list = Question.objects.exclude(ques_type='99')
    return render(request, 'sqltrainapp/personinfo/T_show_Q.html', {'list': list, 'user': user})


# @check_type_2
# def submitques(request):
#     user = User.objects.get(user_name=request.session.get('user_name'))
#     return render(request, 'sqltrainapp/personinfo/submitques.html', {'list': list, 'user': user})


@check_type_3
def S_pass_Q(request):
    list = Question.objects.exclude(ques_type='99')
    if request.method == "POST":
        selection = request.POST['selection']
        key = request.POST['key']
        selecttype = request.POST['selecttype']
        if selecttype:
            list = list.filter(ques_type=selecttype)
        if key:
            if selection == 'ques_id':
                list = list.filter(ques_id=key)
            if selection == 'ques_title':
                list = list.filter(ques_title__contains=key)

    user = User.objects.get(user_name=request.session.get('user_name'))
    list = list.filter(doques__someone_id=user.user_id).filter(doques__result_type='通过')
    return render(request, 'sqltrainapp/personinfo/S_pass_Q.html', {'list': list, 'user': user})


@check_type_3
def S_fail_Q(request):
    list = Question.objects.exclude(ques_type='99')
    if request.method == "POST":
        selection = request.POST['selection']
        key = request.POST['key']
        selecttype = request.POST['selecttype']
        if selecttype:
            list = list.filter(ques_type=selecttype)
        if key:
            if selection == 'ques_id':
                list = list.filter(ques_id=key)
            if selection == 'ques_title':
                list = list.filter(ques_title__contains=key)

    user = User.objects.get(user_name=request.session.get('user_name'))
    list = list.filter(doques__someone_id=user.user_id).filter(doques__result_type='失败')
    return render(request, 'sqltrainapp/personinfo/S_fail_Q.html', {'list': list, 'user': user})


@check_type_3
def S_his(request):
    user = User.objects.get(user_name=request.session.get('user_name'))
    list = Doques.objects.filter(someone_id=user.user_id)
    if request.method == "POST":
        selection = request.POST['selection']
        key = request.POST['key']
        if key:
            if selection == 'run_id':
                list = list.filter(run_id=key)
            if selection == 'answ_content':
                list = list.filter(answ_content__contains=key)
    return render(request, 'sqltrainapp/personinfo/S_his.html', {'list': list, 'user': user})


# 查询
def A_select_T(request):
    selection = request.POST['selection']
    key = request.POST['key']
    list = User.objects.filter(user_type='2')
    if key:
        if selection == 'user_id':
            list = list.filter(user_id=key)
        if selection == 'user_name':
            list = list.filter(user_name__contains=key)
    user = User.objects.get(user_name=request.session.get('user_name'))
    return render(request, 'sqltrainapp/personinfo/A_manage_T.html', {'list': list, 'user': user})


def A_select_S(request):
    selection = request.POST['selection']
    key = request.POST['key']
    list = User.objects.filter(user_type='2')
    if key:
        if selection == 'user_id':
            list = list.filter(user_id=key)
        if selection == 'user_name':
            list = list.filter(user_name__contains=key)
    user = User.objects.get(user_name=request.session.get('user_name'))
    return render(request, 'sqltrainapp/personinfo/A_manage_S.html', {'list': list, 'user': user})
#
def T_select_S(request):
    selection = request.POST['selection']
    key = request.POST['key']
    list = User.objects.filter(user_type='3')
    if key:
        if selection == 'user_id':
            list = list.filter(user_id=key)
        if selection == 'user_name':
            list = list.filter(user_name__contains=key)
    user = User.objects.get(user_name=request.session.get('user_name'))
    return render(request, 'sqltrainapp/personinfo/T_show_S.html', {'list': list, 'user': user})


def T_select_Q(request):
    selection = request.POST['selection']
    key = request.POST['key']
    selecttype = request.POST['selecttype']
    list = Question.objects.exclude(ques_type='99')
    if selecttype:
        list = list.filter(ques_type=selecttype)
    if key:
        if selection == 'ques_id':
            list = list.filter(ques_id=key)
        if selection == 'ques_title':
            list = list.filter(ques_title__contains=key)
    user = User.objects.get(user_name=request.session.get('user_name'))
    return render(request, 'sqltrainapp/personinfo/T_show_Q.html', {'list': list, 'user': user})
