from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models  import CustomUser


class CustomUserAdmin(UserAdmin):
    
    list_display        = ('email', 'is_admin', 'user_type') 
    search_fields       = ('email', 'is_admin', 'user_type')
    ordering            = ('email',)
    readonly_fields     = ('date_joined', )
    
    fieldsets           = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'user_type', 'date_joined', )}), 
        # To call non-editable attributes, you should set 'readonly_fields' above..
    )
    
    add_fieldsets       = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    filter_horizontal   = ()
    list_filter = ('is_admin',)
    
admin.site.register(CustomUser, CustomUserAdmin)