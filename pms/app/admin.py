from django.contrib import admin
from django import forms
from app.models import CustomUser, Usertype, Department, Appraisal, Unit

class MyForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True):
        user = super(MyForm, self).save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = MyForm
    list_display = ('ippis_no', 'first_name', 'last_name', 'usertype')

    class Media:
        js = ('admin_js/usermodel.js', 'admin_js/common.js',)

admin.site.register(Usertype)
admin.site.register(Department)
admin.site.register(Unit)
admin.site.register(Appraisal)
