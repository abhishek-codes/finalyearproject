from django import forms
from .models import User_detail

class UserPageForm(forms.ModelForm):
    class Meta:
        model = User_detail
        fields = ['name','gender','dob','bio','phone','profile_picture','email']