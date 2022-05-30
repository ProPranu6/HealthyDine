from django import forms
from .models import PremiumUser, RegularUser

class SignupFormReg(forms.Form):
    user_id = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30,widget=forms.PasswordInput)
    mail_id = forms.CharField(max_length=30)
    contact_no = forms.IntegerField()
    location = forms.CharField(max_length=30)
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get("user_id")
        password = cleaned_data.get("password")
        contact_no = cleaned_data.get("contact_no")
        
        if len(PremiumUser.objects.raw("select * from user_premiumuser where user_id = %s and password = %s", [user_id, password])) !=0 or len(RegularUser.objects.raw("select * from user_regularuser where user_id = %s and password = %s", [user_id, password])) !=0 :
            
            raise forms.ValidationError(
                    "user_id-password combination already exists"
                )
        if len(PremiumUser.objects.raw("select * from user_premiumuser where contact_no = %s", [contact_no])) !=0 or len(RegularUser.objects.raw("select * from user_regularuser where contact_no = %s", [contact_no])) !=0:
            raise forms.ValidationError(
                    "phonenumber already already exists"
                )

        return cleaned_data

class SignupFormPrem(SignupFormReg):
    height = forms.FloatField()
    weight = forms.FloatField()
    calories_intake = forms.FloatField(initial=2500)
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get("user_id")
        password = cleaned_data.get("password")
        contact_no = cleaned_data.get("contact_no")
        
        if len(PremiumUser.objects.raw("select * from user_premiumuser where user_id = %s and password = %s", [user_id, password])) !=0 or len(RegularUser.objects.raw("select * from user_regularuser where user_id = %s and password = %s", [user_id, password])) !=0 :
            
            raise forms.ValidationError(
                    "user_id-password combination already exists"
                )
        if len(PremiumUser.objects.raw("select * from user_premiumuser where contact_no = %s", [contact_no])) !=0 or len(RegularUser.objects.raw("select * from user_regularuser where contact_no = %s", [contact_no])) !=0:
            raise forms.ValidationError(
                    "phonenumber already already exists"
                )

        return cleaned_data

class LoginForm(forms.Form):
    user_id = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)