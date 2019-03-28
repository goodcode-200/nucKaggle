from django.contrib import admin
from .models import EmailVerifyRecord

# Register your models here.
@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
	list_display = ('code','email')