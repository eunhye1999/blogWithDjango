from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse 

# from django.views import generic

from django.contrib.auth.models import User
from .models import Blog, Comment

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
    # can Edot Content
    blog = get_object_or_404(Blog, pk=pk)
    user_check = get_object_or_404(User, pk=blog.user_id) # get name user form blog
    if((request.user.has_perm('blog.change_blog') and str(user_check.username) == str(request.user)) or 'admin' == str(request.user)):
        edit = True
    else:
        edit = False

    data = {
        'blog': blog, 
        'credit':user_check.username ,
        'edit': edit,
        'user':{
            'user_name': request.user ,
            'status_login': sessionResult(request)
            },
        'user_delete_comment' : 0,
        'comment': False
        }
        
    # can Edot Comment
    if request.session.keys():
        data['comment'] = True
        if 'admin' == str(request.user):
            data['user_delete_comment'] = True
        elif request.user.has_perm('blog.delete_comment'):
            data['user_delete_comment'] = int(request.session['_auth_user_id'])
            
            
    print(data['user_delete_comment'])
    return render(request, 'blog/detail.html', data)

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
        blog = Blog(title = request.POST['title'], content = request.POST['content'], user_id=request.session['_auth_user_id'])
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
        return HttpResponseRedirect(reverse('blog:index'))

def addcomment(request,blog_id):
    print("addcomment")
    if(request.method == "POST"):
        comment = Comment(content_id=blog_id,  comment= request.POST['comment'], user_id=request.session['_auth_user_id'])
        comment.save()
        return HttpResponseRedirect(reverse('blog:detail', args=(blog_id,)))
    else:
        return HttpResponseRedirect(reverse('blog:index'))

def search(request):
    print("search")
    if(request.method == "POST"):
        if(request.POST['search'] == ''):
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            # user_check = get_object_or_404(User, username=request.POST['search'])
            # print(user_check.id)
            # blog = Blog.objects.all().filter(user_id=user_check.id)
            # blog.objects.all()
            # print('asedasdasdasasdsadasddas')
            # print(blog)
            # print('asedasdasdasdas')
            # for blog in blog:
            #     print(blog)
            return HttpResponseRedirect(reverse('blog:searched', args=(request.POST['search'],)))
    else:
        return HttpResponseRedirect(reverse('blog:index'))

def searchAuthor(request, search):
    print("searchAuthor")
    try:
        user_check = get_object_or_404(User, username=search)
        blog = Blog.objects.all().filter(user_id=user_check.id)
        return render(request, 'blog/searchAuthor.html', {'list' : blog, 'author':search, 'user' : { 'user_name': request.user ,'status_login': sessionResult(request)}})
    except:
        print('ssadasd')
        return render(request, 'blog/searchAuthor.html', {'user' : { 'user_name': request.user ,'status_login': sessionResult(request)}})
    