from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    model = Usuario
    # Esto muestra tus campos personalizados en el formulario de edición del admin
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra', {'fields': ('biografia', 'fecha_nacimiento', 'avatar')}),
    )

admin.site.register(Usuario, CustomUserAdmin)