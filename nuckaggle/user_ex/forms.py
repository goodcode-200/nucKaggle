from django import forms
from captcha.fields import CaptchaField

class IdentifyForm(forms.Form):
	email=forms.EmailField(required=True)
	captcha=CaptchaField(error_messages={'invalid':'验证码错误'})