from django import forms
from django.contrib.auth.hashers import check_password
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    # Campo adicional para confirmar contraseña
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        }),
        label='Confirmar Contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password_hash', 'rol']
        labels = {
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'password_hash': 'Contraseña',
            'rol': 'Rol de Usuario',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'password_hash': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu contraseña'
            }),
            'rol': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password_hash')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if password and confirmar_password:
            if password != confirmar_password:
                raise forms.ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        }),
        label='Correo Electrónico'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        }),
        label='Contraseña'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                usuario = Usuario.objects.get(email=email)
                if not check_password(password, usuario.password_hash):
                    raise forms.ValidationError("Credenciales incorrectas")
                cleaned_data['usuario'] = usuario
            except Usuario.DoesNotExist:
                raise forms.ValidationError("Credenciales incorrectas")
        
        return cleaned_data
    
class AnimeSearchForm(forms.Form):
    query = forms.CharField(
        label='Buscar Anime',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Attack on Titan'})
    )