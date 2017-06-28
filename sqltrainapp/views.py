from django.shortcuts import render
from .form import register_f, login_f
from .models import User
from django.http import HttpResponseRedirect


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


@check
def login(request):
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
