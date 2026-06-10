from django import forms 
from cash_management.models import*
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta : 
        model = User
        fields = ['username','email','password1','password2']


class LoginForm(AuthenticationForm):
    pass 


class ProfileForm(forms.ModelForm):
    class Meta:
        model = InfoModel
        fields = '__all__'
        exclude = ['user']


class AddCashForm(forms.ModelForm):
    class Meta:
        model = AddCash
        fields=['source','amount','description']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount','description']