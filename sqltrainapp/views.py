import json

from django.shortcuts import render
from .form import register_f, login_f
from .models import User, Question, Doques
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
import operator





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
            return render(x, 'sqltrainapp/login.html')  # 如果没有登录，则跳转到登录页面

    return wrapper


# @check
def login(request):
    print('[Info    ] you are login')
    return render(request, 'sqltrainapp/index.html')


def login_detail(request):
    if request.method == 'POST':
        # Django获取表单中值的方法
        r = request.POST
        f = login_f(r)
        if f.is_valid():
            user_name = f.cleaned_data.get('user_name')
            request.session['user_name'] = user_name  # 把用户名放入session中
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
        id = User.objects.raw("Select max(user_id) form User")
        for x in id:
            print(x)

        u = User(user_name=r['user_name'], pwd=r['pwd'], user_type=2,
                 school=r['school'], faculties=r['faculties'], cls=r['cls'])
        if f.is_valid():  # 验证请求的内容和Form里面的是否验证通过。通过是True，否则False。
            # print("123123123",f.cleaned_data['user_name'])  # cleaned_data类型是字典，里面是提交成功后的信息。
            u.save()
            return render(request, 'sqltrainapp/login.html', {"msg": '注册成功，请登录'})
        else:  # 错误信息包含是否为空，或者符合正则表达式的规则
            print(type(f.errors), f.errors)  # errors类型是ErrorDict，里面是ul，li标签
            return render(request, "sqltrainapp/register.html", {"error": f.errors, 'f': f, "user": u})
    else:
        return render(request, "sqltrainapp/register.html")


@check
def logout(request):
    try:
        del request.session['user_name']
    except KeyError:
        pass
    return render(request, 'sqltrainapp/login.html', {"msg": '已注销'})


def index(request):
    return render(request, 'sqltrainapp/index.html')


@check
def Getting_Started(request):
    return render(request, 'sqltrainapp/Getting_Started.html')


@check
def basic(request):
    return render(request, 'sqltrainapp/questions/basic.html')

@check
def selectall(request):
    question = Question.objects.get(ques_type=101)
    # question = Question.objects.all()
    qid = question.ques_id
    question_content = question.ques_content
    sql = question.answer
    print("[Info    ]" + sql)
    print('[Info    ]' + str(qid))
    #members = Question.objects.raw("SELECT * FROM sqltrainapp_question")    # [:] 注释这里就会从set变成list
    # 返回的默认是list
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqltrainapp_question")
    members = cursor.fetchall()
    print('[Info    ]' + str(type(members)))    # <class 'django.db.models.query.RawQuerySet'>
    # print('[Info    ]' + str(members))
    # l = len(members)
    for x in members:
        print('[Info    ]' + str(x))
    return render(request, 'sqltrainapp/questions/basic/selectall.html', {
                                                    'members': members,
                                                    'question_content': question_content,
                                                    'sql_raw': sql,
                                                    'qid':qid
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
        if cmpresult==False :
            pass
        print('[Info    ]' + str(cmpresult))
        # 对set进行比较，
        # 先比较长度
        # 再进行交集运算找出相同的set集合，然后就可以找出不同的地方

        # 给出错误原因，提示信息，放入cmpresult，并写入数据库，需要传过来用户的id，问题的id，
        # 写入 错误原因 及 用户的答案
        uname=request.session.get('user_name')
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
        ret = { 'result':row,
                'cmpresult': cmpresult
        }
        return HttpResponse(json.dumps(ret), content_type='application/json')
        #return HttpResponse(ret)

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


@check
def joins(request):
    return render(request, 'sqltrainapp/questions/joins.html')


@check
def aggregates(request):
    return render(request, 'sqltrainapp/questions/aggregates.html')


@check
def date(request):
    return render(request, 'sqltrainapp/questions/date.html')


@check
def string(request):
    return render(request, 'sqltrainapp/questions/string.html')


@check
def recursive(request):
    return render(request, 'sqltrainapp/questions/recursive.html')


@check
def about(request):
    return render(request, 'sqltrainapp/about.html')


@check
def options(request):
    return render(request, 'sqltrainapp/options.html')


@check
def moban(request):
    return render(request, 'sqltrainapp/moban.html')
