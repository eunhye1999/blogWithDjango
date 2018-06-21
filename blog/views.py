from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse 

from django.contrib.auth.models import User
# from django.views import generic

from .models import Blog

def sessionResult(request):
    if request.session.keys():
        return True
    else: 
        return False

def index(request):
    if request.session.keys():
        login = True
    else: 
        login = False
        
    list_title = Blog.objects.order_by('-created_at')
    return render(request, 'blog/index.html', {'list' : list_title, 'user' : { 'user_name': request.user ,'status_login': sessionResult(request)}})

def addForm(request):
    print('addForm')
    if((request.user.has_perm('blog.add_blog') or 'admin' == str(request.user))):
        edit = True
    else:
        edit = False

    return render(request, 'blog/formAddCon.html' , {'state' :  edit ,'user' : { 'user_name': request.user ,'status_login': sessionResult(request)}} )

def detail(request,pk):

    blog = get_object_or_404(Blog, pk=pk)
    user_check = get_object_or_404(User, pk=blog.user_id) # get name user
    if((request.user.has_perm('blog.change_blog') and str(user_check.username) == str(request.user)) or 'admin' == str(request.user)):
        edit = True
    else:
        edit = False

    print('blog.user_id :', blog.user_id)
    print('blog.title :',blog.title)
    print('blog.title :',blog.content)
    return render(request, 'blog/detail.html', {'blog': blog, 'credit':user_check.username ,'edit': edit, 'user':{ 'user_name': request.user ,'status_login': sessionResult(request)}})

def editCon(request,pk):
    print('editCon')
    blog = Blog.objects.get(pk=pk)
    print('blog edit : id ',blog.id)
    print('blog edit : title ',blog.title)
    return render(request, 'blog/edit.html', {'blog': blog, 'user':{ 'user_name': request.user ,'status_login': sessionResult(request)}})

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
        return HttpResponseRedirect(reverse('blog:index'))
    
def addCon(request):
    print('addCon')
    try:
        print('add Title : ',request.POST['title'])
        print('add Content : ',request.POST['content'])
        blog = Blog(title = request.POST['title'], content = request.POST['content'], user_id=request.session['_auth_user_id'] )
    except (KeyError):
        pass
    else:
        blog.save()
        return HttpResponseRedirect(reverse('blog:index'))

def deleteCon(request,pk):
    print("deleteCon")
    try:
        blog = Blog.objects.get(pk=pk)
    except (KeyError):
        pass
    else:
        blog.delete()
        # blog.save()
        return HttpResponseRedirect(reverse('blog:index'))