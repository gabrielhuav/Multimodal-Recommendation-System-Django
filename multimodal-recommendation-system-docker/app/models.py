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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos')
    anime_id = models.IntegerField()  # Corresponde a mal_id de Jikan API
    anime_titulo = models.CharField(max_length=255)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'anime_id') # Evita que un usuario marque el mismo anime como favorito múltiples veces
        db_table = 'favoritos_anime'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f"{self.anime_titulo} (Favorito de {self.usuario.nombre})"