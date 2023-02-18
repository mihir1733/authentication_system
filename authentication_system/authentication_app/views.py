from django.shortcuts import render,redirect
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from authentication_system import settings
from django.core.mail import send_mail
 


# Create your views here.

def home(request):
    return render(request,'index.html')





def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists !")

        if User.objects.filter(email=email):
            messages.error(request,"Email already registered !")

        if len(username)>10:
            messages.error(request,"Username must be under 10 characters !")

        if pass1 != pass2:
            messages.error(request,"Password didn't match !")

        if not username.isalnum():
            messages.error(request,"Username mustbe alpha numeric !")
            return redirect('home')
        

        user = User.objects.create_user(username,email,pass1)
        user.first_name = fname
        user.last_name = lname
        user.is_active = False

        user.save()

        messages.success(request,"Your Account has been created successfully ! Please check your email.")

        #Welcome Email

        subject = "Welcome to my Authentication System - Djnago Login !"

        message = "hello" + " " +user.first_name + "!! \n" + "Welcome to my project!! \n  Your account is created successfully :) \nThank You ! for visiting my website..\n\n Pithva Mihir"

        from_email = settings.EMAIL_HOST_USER

        to_email_list = [user.email]

        send_mail(subject,message,from_email,to_email_list,fail_silently=True)

        
        return redirect('signin')

    return render(request,'signup.html')







def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request,'index.html',{'fname':fname})
        else:
            messages.error(request,"Invalid credentials")

    return render(request,'signin.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully !!")
    return redirect('home')