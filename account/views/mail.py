from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from ..models.store_token import Store_Token
from ..tokens.tokens import token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from smtplib import SMTPException
import hashlib , base64


timeout_in_mins=10
timeout_in_hours=None
timeout_in_days=None
class Mail():

    def __init__(self, request , user, template_name="body_confirm_mail.html" , timeout="10 mins"):
        """
            to setting the timeout should be string and add the number with space with three words should 
            be choose from him ('min(s)' , 'hour(s)' , 'day(s)')
            the default timeout is 10 mins.

        """
        self._request       = request
        self._user          = user
        self._template_name = template_name 
        self._timeout       = timeout
        

    
    def send_mail(self , to , from_email=None , subject="Activation Account", message=None):
        
        if isinstance(to , str):
            to = [to]
    
        sending_mail = EmailMessage(subject=subject ,
                                    body=self._make_body_string(message) , from_email=from_email , to=to)

        try:
            sending_mail.send()
            return True
        except SMTPException as e:
            return e
            
        
    
    def check_token(self , token):
        """
            check the time of the token is expired or still alive and return bool
        """
        timeout_mins , timeout_hours , timeout_days= None , None , None
        time , op = self._timeout.split(" ")

        if op == 'mins' or op == 'min':
            timeout_mins= int(time)
            timeout_in_mins = timeout_mins
        elif op == 'hours' or op == 'hour':
            timeout_hours = int(time)
            timeout_in_hours = timeout_hours
        elif op == 'days' or op == 'day':
            timeout_days = int(time)
            timeout_in_days = timeout_days
      
        return token_generator.check_token(token , {"pk": self._user.pk , "username": self._user.username},
                                        timeout_min=timeout_mins , timeout_hours=timeout_hours ,
                                        timeout_days=timeout_days)


    def check_user_hash(self , hashed):
        """
            return Boolean if hashed are same pk of user of not
        """ 
        _ , hashed = hashed.split("&$4/-")

        return self._make_hash_user(check=True) == hashed


    def _get_current_site(self):
        
        """
            return the domain of the site
        """
        return get_current_site(self._request).domain

    def _make_token(self):
        """
            generate token with pk and username of user that are registered and return the hash token
        """

        return token_generator.make_token({"pk": self._user.pk , "username": self._user.username})

    def _make_hash_user(self , check=False):
        """
            get the pk of the user and generate hash and return it
        """
        print(len(base64.b85encode(force_bytes(self._user.pk)).decode("utf-8")))
        if check:
            return hashlib.sha256(force_bytes(self._user.pk)).hexdigest()

        return base64.b85encode(force_bytes(self._user.pk)).decode("utf-8") + "&$4/-" + hashlib.sha256(force_bytes(self._user.pk)).hexdigest()
    

    def _make_body_string(self , message):
        """
            make template as a string and return it after converted
        """
        return render_to_string( self._template_name , self._make_context(message) )

    def _make_context(self , message):
        """
            make context that will be pass into a body and return it 
        """
        token = str( self._make_hash_user()) + "/=" + str( self._make_token())
        store_token = Store_Token.objects.create(token=token)
        store_token.save()
        return {
            'user': self._user,
            'message': message,
            'domain': self._get_current_site(),
            'token': token,
            'timeout': self._timeout,
        }



def get_user_from_hash(hashed):
    """
        it use for get the primary from hashed token and return it after decode the token
    """
    user , _ = hashed.split("&$4/-")
    return int( base64.b85decode(force_bytes(user)).decode("utf-8"))



def check_and_get_data_from_token(token , method="GET"):

    if method == "POST":
        pk = get_user_from_hash(token)
        return User.objects.get(pk=pk)
        
    try:
        token_exist = Store_Token.objects.get(token=token)
        pk = get_user_from_hash(token)
        _ , token = token.split("/=")
        user= User.objects.get(pk=pk)
        
        check = token_generator.check_token(token , user={"pk":pk , "username":user.username} ,
                                        timeout_min=timeout_in_mins , timeout_hours=timeout_in_hours ,
                                        timeout_days=timeout_in_days)


        if not check:
            token_exist.delete()
            return user

        token_exist.delete()
        return False

    except Store_Token.DoesNotExist:
        return False
        

