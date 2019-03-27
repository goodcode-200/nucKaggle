from django import forms
from captcha.fields import CaptchaField

class IdentifyForm(forms.Form):
	email=forms.EmailField(required=True)
	captcha=CaptchaField(error_messages={'invalid':'验证码错误'})

class ResetForm(forms.Form):
	newpwd1=forms.CharField(required=True,min_length=6,error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
	newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})