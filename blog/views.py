from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse 

# from django.views import generic

from django.contrib.auth.models import User
from .models import Blog, Comment
from django.core.paginator import Paginator

def auth_permission(request, permission):
    print('auth_permission') 
    result = False
    if(request.user.has_perm(permission) or 'admin' == str(request.user)):
        result = True
    else:
        result = False
    return result 

def sessionResult(request):
    if request.session.keys():
        return True
    else: 
        return False

def index(request):
    print('index')
    list_title = Blog.objects.order_by('-created_at')
    paginator = Paginator(list_title, 5)

    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    return render(request, 'blog/index.html', {'list' : blogs, 'user' : { 'user_name': request.user ,'status_login': sessionResult(request)}})

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
        result = auth_permission(request, 'blog.change_blog')
        blog = Blog.objects.get(pk=pk)
    except (KeyError):
        pass
    else:
        if(result):
            blog.title = request.POST['title']
            blog.content = request.POST['content']
            blog.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blog/errorPerm.html')
    
def addCon(request):
    print('addCon')
    try:
        result = auth_permission(request, 'blog.add_blog')
        print('add Title : ',request.POST['title'])
        print('add Content : ',request.POST['content'])
    except (KeyError):
        pass
    else:
        if(result):
            blog = Blog(title = request.POST['title'], content = request.POST['content'], user_id=request.session['_auth_user_id'])
            blog.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blog/errorPerm.html')

def deleteCon(request,pk):
    print("deleteCon")
    try:
        result = auth_permission(request, 'blog.delete_blog')
        blog = Blog.objects.get(pk=pk)
    except (KeyError):
        pass
    else:
        if(result):
            blog.delete()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            print('asdsadasd')
            return render(request, 'blog/errorPerm.html')

def comment(request,blog_id):
    print("addcomment")
    result = auth_permission(request, 'blog.add_comment')
    if(request.method == "POST" and result == True):
        comment = Comment(content_id=blog_id,  comment= request.POST['comment'], user_id=request.session['_auth_user_id'])
        comment.save()
        return HttpResponseRedirect(reverse('blog:detail', args=(blog_id,)))
    else:
        return render(request, 'blog/errorPerm.html')

def delComment(request,blog_id,comment_id):
    print("delComment")
    try:
        result = auth_permission(request, 'blog.delete_comment')
        comment = Comment.objects.get(pk=comment_id)
    except (KeyError):
        pass
    else:
        if(result): 
            comment.delete()
            return HttpResponseRedirect(reverse('blog:detail', args=(blog_id,)))
        else:
            return render(request, 'blog/errorPerm.html')


def search(request):
    print("search")
    if(request.method == "POST"):
        if(request.POST['search'] == ''):
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return HttpResponseRedirect(reverse('blog:searched', args=(request.POST['search'],)))
    else:
        return HttpResponseRedirect(reverse('blog:index'))



def searchAuthor(request, search):
    print("searchAuthor")
    data = {
        # 'list' : listEmp, 
        'author':search, 
        'user' : { 
            'user_name': request.user ,
            'status_login': sessionResult(request)
            }
        }
        
    dictUser = {}
    try:
        user_check = User.objects.filter(username__contains=search)
        print(user_check)
        for user in user_check:
            dictBlog = {}
            blogs = Blog.objects.all().filter(user_id=user.id)
            if(blogs):
                for blog in blogs:
                    dictBlog[str(blog.id)] = blog
                dictUser[str(user)] = dictBlog

        data = {
            'dictUser' : dictUser, 
            'author':search, 
            'user' : { 
                'user_name': request.user ,
                'status_login': sessionResult(request)
                }
            }
        print('pass')
        return render(request, 'blog/searchAuthor.html', data)
    except:
        print('ssadasd')
        return render(request, 'blog/searchAuthor.html', {'user' : { 'user_name': request.user ,'status_login': sessionResult(request)}})

