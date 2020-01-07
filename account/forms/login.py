from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import forms  , UsernameField


class UserLoginForm(forms.Form):
    username = UsernameField(label='Username',widget=forms.TextInput(attrs={'autofocus': True ,'placeholder': 'Username'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password' , 'placeholder':'Password'}),
    )

    error_message = {
        'username': _('The %(username)s doesn\'t Exists Please Register to come in our members ^_^'),
        'password': 'Incorrect password. please Try again with correct Password',  
        
    }

    def clean(self, *args , **kwargs):
        
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get('password')

        try:

            user = User.objects.get(username=username)
            if not user.is_active:
                raise forms.ValidationError("This Account isn't Active please Activate your account to login")
            
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_message['username'] , params={'username': username})


        if  not user.check_password(password):
            raise forms.ValidationError(self.error_message['password'] , code=self.error_message['password'])
            
        return super(UserLoginForm, self).clean(*args , **kwargs)




