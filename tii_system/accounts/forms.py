from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    first_name  = forms.CharField(max_length=30, required=True, help_text='Required. Your first name.',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name   = forms.CharField(max_length=30, required=True, help_text='Required. Your last name.',widget=forms.TextInput(attrs={'class':'form-control'}))
    email       = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']  = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class LogInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError('Please enter a correct username \
                    and password. Note that both fields may be case-sensitive.')

        return super(LogInForm, self).clean(*args, **kwargs)