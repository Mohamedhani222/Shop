from time import sleep
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from .forms import *
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect ('admin-dash')
                # Redirect to a success staff page.
            else:
                login(request, user)
                return redirect ('index')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request, 'login.html')





def register(request):
    if request.method == 'POST' :
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login( request , user )
            return redirect('index')
    else :
        form =RegisterForm()

    return render(request , 'registration/register.html' , {'form' : form })
    



def logout_view(request):
    logout(request)
    return redirect('home')



