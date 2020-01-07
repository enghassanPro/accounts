from .mail import Mail , get_user_from_hash , check_and_get_data_from_token
from django.shortcuts import render , redirect
from ..forms.register import UserRegisterForm
from django.contrib.auth.models import User
from ..tokens.tokens import token_generator
from django.contrib import messages

def register(request , tk):
    
    token = token_generator.make_token()
    
    if request.user.is_authenticated:
        return  redirect("auth:view" , token)# the path will be changed

    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send = send_mail(request , user)
        if send == True:
            messages.success(request , "Confirmation Email has been sent check your inbox mail.")
            return redirect("auth:login" , token)

        messages.error(request , "Error!"+ send)
        return redirect("auth:login" , token)
    return render(request , "registration/register.html" ,{"form":form , "token": token})

def send_mail(request , user):

    token = token_generator.make_token()
    mail = Mail(request , user)
    return mail.send_mail(to=user.email , subject="Confirmation Account")


def request_active_email(request , token):

    new_token = token_generator.make_token()
    check = check_and_get_data_from_token(token)
    if not check:
        messages.error(request , "Invalid Token Try again with send new mail")
        return redirect("auth:login" , new_token)
    
    if not check.is_active:
        check.is_active = True
        check.save()
        messages.warning(request , "The email has been Active You can login Now.")
        return redirect("auth:login" , new_token)
    
    messages.error(request , "Invalid Token")
    return redirect("auth:login" , new_token)

    # pk = get_user_from_hash(token)
    # user = User.objects.get(pk=pk)
    # if user.is_active:
    #     messages.error(request , "Inavlid Token")
    #     return redirect("auth:login" , new_token)

    # _ , token = token.split("/=")
    # check = token_generator.check_token(token , {"pk":pk , "username":user.username})
    # if not check:
    #     user.is_active = True
    #     user.save()
    #     messages.success(request , "The email has been Activate You can login Now.")
    #     return redirect("auth:login" , new_token)
    

