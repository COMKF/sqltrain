from django.shortcuts import render

# Create your views here.

def index(request):
    value = True
    content = {
        'key':value
    }
    return render(request, 'sqltrainapp/index.html', content)

def basic(request):
    content = {
        'key': 1
    }
    return render(request, 'sqltrainapp/questions/basic/basic.html', content)

def selectall(request):
    content = {
        'key': 1
    }
    return render(request, 'sqltrainapp/questions/basic/selectall.html', content)