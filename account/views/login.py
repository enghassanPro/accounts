from django.contrib.auth import authenticate, login
from django.shortcuts import render ,redirect 
from ..tokens.tokens import token_generator
from django.contrib.auth.models import User
from ..forms.login import UserLoginForm
from django.contrib import messages
from .mail import Mail

def load(request):

    token = token_generator.make_token()
    return redirect("auth:login" , token)

def loginAuth(request , tk):
    token = token_generator.make_token()

    if request.user.is_authenticated:
        return  redirect("auth:view" , token)# the path will be changed

    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(username=form.cleaned_data.get('username') , password=form.cleaned_data.get('password'))
        login(request , user)
        return redirect("auth:view" , token)
    
    if form.errors: 
        get_err = list( form.errors['__all__'].as_data()[0] )[0]
        if "Active" in get_err:
            return render(request , "registration/login.html" , {"form":form , "send":request.POST['username'] , "token": token} )
    return render(request , "registration/login.html" , {"form":form , "token": token} )


def home(request , tk):

    token = token_generator.make_token()
    return render(request , "home.html" , { "token": token} )


def resend_email(request , username):
    
    token = token_generator.make_token()
    user = User.objects.get(username=username)
    mail = Mail(request , user)
    send = mail.send_mail(to=user.email , subject="Resend Confirmation Account")
    if send == True:
        messages.success(request , "Confirmation Email has been sent check your inbox mail.")
        return redirect("auth:login" , token)

    messages.error(request , "Error!"+ send)
    return redirect("auth:login" , token)