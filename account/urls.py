from django.conf.urls import url , include
from django.conf.urls.static import static
from django.contrib.auth import settings
from .views import (
    login,
    register,
    logout,
    mail,
    reset_password,
)

# register namespace
app_name='auth'

token = "(?:tk=(?P<tk>[0-9A-Za-z]{1,9}[?=]{1,2}[0-9A-Za-z]{1,20}[0-9A-Za-z]{1,50}))/$"
token_mail = "(?:confirm=(?P<token>[a-zA-Z0-9!#$%&()*+-;<=>?@^_`{|}~]+[/-]{1,2}[a-zA-Z0-9]{1,64}[/=]{1,2}[0-9A-Za-z]{1,9}[?=]{1,2}[0-9A-Za-z]{1,20}[0-9A-Za-z]{1,50}))/$"

urlpatterns = [
    url(r'^$' , login.load , name="load"),
    url(r'^home/'+ token , login.home , name="view"),
    url(r'^logout/'+ token , logout.logoutAuth , name="logout"),
    url(r'^login/'+ token , login.loginAuth , name="login"),
    url(r'^register/'+ token , register.register , name="register"),
    url(r'^mail/send/(?:username=(?P<username>[a-zA-Z0-9_-]+))/$' , login.resend_email , name="send"),
    url(r'^mail/active/' + token_mail , register.request_active_email , name="active"),
    url(r'^reset-password/' + token , reset_password.reset , name="reset"),
    url(r'^reset-password/new/' + token_mail , reset_password.new_password , name="reset_new"),
    url(r'^oauth/' , include('social_django.urls' , namespace="social")),
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
