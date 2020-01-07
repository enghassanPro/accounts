from django.contrib.auth.models import User 
from django.contrib.auth.forms import forms

class UserRegisterForm(forms.ModelForm):
    
    first_name = forms.CharField(label="First Name" ,max_length=30 , min_length=4 ,
                                widget=forms.TextInput(attrs={'autofocus': True ,'placeholder': 'First Name'}),
                                help_text='should enter at least 4 characters and at most 30 characters')
    last_name  = forms.CharField(label="Last Name" ,max_length=150 , min_length=4 ,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
                                help_text='should enter at least 4 characters and at most 150 characters')
    email      = forms.EmailField(label="Email",max_length=150 ,
                                widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username   = forms.CharField(label="Username" ,
                                widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                                help_text="Required. 150 characters or fewer.Letters,digits and @/./+/-/_ only.")
    password   = forms.CharField(label="Password" , min_length=8 ,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) ,help_text=[
                                "Your Password can't be too similar to your other personal information.",
                                "Your Password must contain at least 8 characters."
                                "Your Password can't be a commonly used password.",
                                "Your Password can't be entirely numeric."]
                                )
    password1  = forms.CharField(label="Confirm Password" , min_length=8 ,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}) , 
                                help_text="Enter the same password as before,for validtion.") 
    
    errors_messages = {
        'password_mismatch': "The two password fields didn’t match.",
    }
    
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'email' , 'password']
        
    def clean(self , *args , **kwargs):

        password  = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        email = self.cleaned_data.get('email')

        if password and password1 and password != password1:
            raise forms.ValidationError( self.errors_messages['password_mismatch'], code='password_mismatch' )

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email,That is already taken')

        return super(UserRegisterForm , self).clean(*args , **kwargs)    
    

    def save(self , commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
