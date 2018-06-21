from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User

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

def register(request):
    if(request.method == "POST"):
        return redirect('/blog/')
    elif(request.method == "GET"):
        print("regisForm")
        return render(request, 'account/regisForm.html')