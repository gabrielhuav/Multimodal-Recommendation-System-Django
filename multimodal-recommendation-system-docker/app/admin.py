from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'rol')
    list_filter = ('rol',)
    search_fields = ('nombre', 'email')
    ordering = ('id',)
    
    # Campos de solo lectura para evitar mostrar la contraseña hasheada
    readonly_fields = ('password_hash',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'email')
        }),
        ('Configuración de Cuenta', {
            'fields': ('rol', 'password_hash')
        }),
    )