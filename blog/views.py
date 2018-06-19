from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse 
# from django.views import generic

from .models import Blog

def index(request):
    list_title = Blog.objects.order_by('created_at')
    # print(list_title)
    return render(request, 'blog/index.html', {'list' : list_title})

def addForm(request):
    print('addForm')
    return render(request, 'blog/formAddCon.html')

def detail(request,pk):
    print('detail')
    blog = get_object_or_404(Blog, pk=pk)
    print('blog.title :',blog.title)
    print('blog.title :',blog.content)
    return render(request, 'blog/detail.html', {'blog': blog})

def editCon(request,pk):
    print('editCon')
    blog = Blog.objects.get(pk=pk)
    print('blog edit : id ',blog.id)
    print('blog edit : title ',blog.title)
    return render(request, 'blog/edit.html', {'blog': blog})

def editedCon(request,pk):
    print('editedCon')
    try:
        print('edit Title : ',request.POST['title'])
        print('edit Content : ',request.POST['content'])
        blog = Blog.objects.get(pk=pk)
    except (KeyError):
        pass
    else:
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.save()
        return HttpResponseRedirect('/blog')
    

    

def addCon(request):
    print('addCon')
    try:
        print('add Title : ',request.POST['title'])
        print('add Content : ',request.POST['content'])
        blog = Blog(title = request.POST['title'], content = request.POST['content'])
    except (KeyError):
        pass
    else:
        blog.save()
        return HttpResponseRedirect('/blog')
