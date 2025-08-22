from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    ROLES = [
        ('usuario', 'Usuario'),
        ('administrador', 'Administrador'),
    ]
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.TextField()
    rol = models.CharField(max_length=50, choices=ROLES, default='usuario')
    
    def save(self, *args, **kwargs):
        # Si se está creando un nuevo usuario y la contraseña no está hasheada
        if not self.pk and not self.password_hash.startswith('pbkdf2_'):
            self.password_hash = make_password(self.password_hash)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} ({self.email})"
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Favorito(models.Model):
    TIPO_CONTENIDO = [
        ('anime', 'Anime'),
        ('libro', 'Libro'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos')
    contenido_id = models.CharField(max_length=100)  # mal_id para anime, work_id para libros
    contenido_titulo = models.CharField(max_length=255)
    tipo_contenido = models.CharField(max_length=10, choices=TIPO_CONTENIDO)
    autor = models.CharField(max_length=255, blank=True, null=True)  # Para libros
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'contenido_id', 'tipo_contenido')
        db_table = 'favoritos_contenido'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        if self.tipo_contenido == 'libro':
            return f"{self.contenido_titulo} por {self.autor} (Favorito de {self.usuario.nombre})"
        return f"{self.contenido_titulo} (Favorito de {self.usuario.nombre})"