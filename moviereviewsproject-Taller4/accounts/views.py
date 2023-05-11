from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signup.html',
            {'form':UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html',
                {'form':UserCreateForm,
                'error':'Nombre de usuario ya existente. Intente con uno nuevo.'})
        else:
            return render(request, 'signup.html',
            {'form':UserCreateForm, 'error':'Las contraseñas no coinciden.'})

@login_required       
def logoutaccount(request):
    logout(request)
    return redirect('home')

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'login.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
    if user is None:
        return render(request,'login.html',{'form': AuthenticationForm(),'error': 'El usuario y la contraseña no coinciden.'})
    else:
        login(request,user)
    return redirect('home')