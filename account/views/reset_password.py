from .mail import Mail , get_user_from_hash , check_and_get_data_from_token
from ..forms.reset_password import ResetPasswordForm , NewPasswordForm
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from ..tokens.tokens import token_generator
from django.contrib import messages

def reset(request , tk):
    token = token_generator.make_token()
    form = ResetPasswordForm(request.POST or None)

    if form.is_valid():
        user = User.objects.get(email=form.cleaned_data['email'])
        send = send_mail(request , user , template_name="body_reset_mail.html" , subject="Reset Password")
        if send == True:
            messages.success(request , "The Email has been sent check your inbox.")
            return redirect("auth:login" , token)

        messages.error(request , "Error!"+send)
        return render(request , "registration/reset_password.html" , {"form": form , "token": token})

    return render(request , "registration/reset_password.html" , {"form": form , "token": token})

def send_mail(request , user , template_name , subject):
    
    token = token_generator.make_token()
    mail = Mail(request , user , template_name=template_name)
    return mail.send_mail(to=user.email , subject=subject)

def new_password(request , token):

    new_token = token_generator.make_token()
    
    check = check_and_get_data_from_token(token , method=request.method)
    
    if not check:
        messages.error(request , "Invalid Token Try again with send new mail")
        return redirect("auth:login" , new_token)

    form = NewPasswordForm(request.POST or None)

    if form.is_valid():
        check.set_password(form.cleaned_data['password'])
        check.save()
        messages.success(request , "The Password has been Reset")
        return redirect("auth:login" , new_token)
    
    return render(request, "registration/new_password.html" , {"form":form  , "token": token})