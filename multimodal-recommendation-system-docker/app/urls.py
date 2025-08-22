from django.contrib import admin
from django.urls import path, include
from . import views

# Todas las URLs sin prefijos de idioma
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Para cambio de idioma
    path('', views.index, name='index'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('buscar-anime/', views.buscar_anime, name='buscar_anime'),
    path('buscar-libros/', views.buscar_libros, name='buscar_libros'),
    path('toggle-favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('mis-favoritos/', views.mis_favoritos, name='mis_favoritos'),
    path('recomendaciones/', views.recomendaciones_anime, name='recomendaciones_anime'),
    path('recomendaciones-libros/', views.recomendaciones_libros, name='recomendaciones_libros'),
]