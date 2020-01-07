from django.contrib.auth import logout
from django.shortcuts import redirect 

def logoutAuth(request , tk):
    logout(request)
    return redirect("auth:load")
