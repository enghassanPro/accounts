from django.contrib.auth.models import User 
from django.contrib.auth.forms import forms

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=150 ,
                            widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    def clean(self, *args , **kwargs):

        email = self.cleaned_data.get("email")
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email isn't Found")

        return super(ResetPasswordForm , self ).clean(*args , **kwargs)
        

class NewPasswordForm(forms.ModelForm):
    password   = forms.CharField(min_length=8 , widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) ,
                                help_text=[
                                    "Your Password can't be too similar to your other personal information.",
                                    "Your Password must contain at least 8 characters."
                                    "Your Password can't be a commonly used password.",
                                    "Your Password can't be entirely numeric."]
        )
    password1  = forms.CharField(min_length=8 , widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}) , 
                                 help_text="Enter the same password as before,for validtion.") 
    
    errors_messages = {
        'password_mismatch': "The two password fields didn’t match.",
    }

    class Meta:
        model = User
        fields = ['password']
        
    def clean(self , *args , **kwargs):

        password  = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        
        if password and password1 and password != password1:
            raise forms.ValidationError( self.errors_messages['password_mismatch'], code='password_mismatch' )

        return super(NewPasswordForm ,self).clean(*args , **kwargs)


