from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from . import forms as f

# Create your views here

def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', 
                       {'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], 
                            password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', 
                 {'form':UserCreationForm,
                 'error':'Username already taken. Choose new username.'})
        else:
            return render(request, 'signupaccount.html', 
             {'form':UserCreationForm, 'error':'Passwords do not match'})

def logoutaccount(request):        
    logout(request)
    return redirect('home')

def loginaccount(request):    
    if request.method == 'GET':
        return render(request, 'loginaccount.html', 
                      {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request,'loginaccount.html', 
                    {'form': AuthenticationForm(), 
                    'error': 'username and password do not match'})
        else: 
            login(request,user)
            return redirect('home')
        
@login_required(login_url='signin')
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)        

def edit_user(request,pk):
    user = User.objects.get(id=pk)  
    form = f.edit_user_form(instance=user)
    
    if request.method == 'POST':
        form = f.edit_user_form(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    context = {'user':user,'form':form}
    return render(request,'form_rendering.html',context)