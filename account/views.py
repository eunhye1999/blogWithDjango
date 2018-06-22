from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
from account.forms import SignUpForm

def login(request):
    if(request.method == "POST"):
        user_id = request.POST['id']
        user_pass = request.POST['password']
        print(user_id)
        print(user_pass)

        user = authenticate(request, username=user_id, password=user_pass)
        if user is not None:
            auth_login(request, user)
            return redirect('/blog/')
        else:
            return render(request, 'account/failform.html')
        
    elif(request.method == "GET"):
        print("loginForm")
        return render(request, 'account/loginForm.html')
    
def logout(request):
    auth_logout(request)
    return redirect('/blog/')

def get_permission(perm):
    if(perm == '3'):
        return ['add_blog','change_blog','delete_blog','add_comment','change_comment','delete_comment']
    elif(perm == '2'):
        return ['add_blog','change_blog','delete_blog','delete_comment']
    elif(perm == '1'):
        return ['add_blog','delete_blog','delete_comment']
    elif(perm == '0'):
        return ['delete_comment'] 
    else:
        return []

def register(request):
    if(request.method == "POST"):
        form = SignUpForm(request.POST)
        # print('SAVE already')
        # print(request.POST['perm'])
        
        if form.is_valid():
            form.save()
            print('SAVE already')
            u = User.objects.get(username=request.POST['username'])
            u.is_staff = True
            perms = get_permission(request.POST['perm'])
            print(perms)
            for perm in perms:
                permission = Permission.objects.get(codename=perm)
                u.user_permissions.add(permission)
            print('update permission already')

        else:
            print('testetewtew')
            return render(request, 'account/failformRegis.html')
    elif(request.method == "GET"):
        print("regisForm")
        form = SignUpForm()
        permission = ['add_blog','change_blog','delete_blog','add_comment','change_comment','delete_comment']
        return render(request, 'account/regisForm.html', {'form':form ,'permission': permission})

    return HttpResponseRedirect(reverse('blog:index'))