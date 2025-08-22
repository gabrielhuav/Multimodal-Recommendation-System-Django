# 🎯 Sistema de Búsqueda y Recomendación Multimodal

Un sistema web desarrollado en Django que permite a los usuarios buscar, marcar como favoritos y recibir recomendaciones personalizadas de contenido multimedia. Actualmente implementado con anime (Jikan API) y preparado para expandirse a películas, libros y otros tipos de contenido.

## ✨ Características

### 🔐 Sistema de Autenticación
- Registro e inicio de sesión de usuarios
- Gestión de sesiones segura
- Roles de usuario (Usuario/Administrador)
- Panel de administración de Django

### 🔍 Búsqueda de Contenido
- **Anime**: Búsqueda integrada con Jikan API (MyAnimeList)
- Resultados con imágenes, sinopsis, puntuaciones y detalles
- Filtrado de contenido seguro (SFW)
- **Preparado para**: Películas (TMDB), Libros (OpenLibrary), Música (Spotify), etc.

### ⭐ Sistema de Favoritos
- Marcar/desmarcar contenido como favorito
- Lista personalizada de favoritos por usuario
- Prevención de duplicados automática

### 🎯 Recomendaciones Inteligentes
- Recomendaciones basadas en favoritos del usuario
- Algoritmo que evita sugerir contenido ya marcado
- Rate limiting para APIs externas
- **Futuro**: Machine Learning para mejores recomendaciones

## 🏗️ Arquitectura

### Stack Tecnológico
- **Backend**: Django 4.2+, PostgreSQL
- **Frontend**: Bootstrap 5, Font Awesome
- **APIs**: Jikan (MyAnimeList), preparado para TMDB, OpenLibrary
- **Containerización**: Docker + Docker Compose

### Estructura del Proyecto
```
multimodal-recommendation-system/
├── app/
│   ├── models.py          # Usuario, Favorito
│   ├── views.py           # Lógica de búsqueda y recomendaciones
│   ├── forms.py           # Formularios de usuario y búsqueda
│   ├── templates/         # Templates HTML con Bootstrap
│   └── migrations/        # Migraciones de base de datos
├── docker-compose.yml     # Configuración de servicios
├── Dockerfile            # Imagen de la aplicación
├── requirements.txt      # Dependencias Python
└── README.md
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Docker y Docker Compose instalados
- Puerto 8080 disponible

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/multimodal-recommendation-system.git
cd multimodal-recommendation-system
```

2. **Construir los contenedores**
```bash
docker-compose build
```

3. **Iniciar los servicios**
```bash
docker-compose up -d
```

4. **Ejecutar migraciones**
```bash
docker-compose run web python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
docker-compose run web python manage.py createsuperuser
```

6. **Acceder a la aplicación**
- **Aplicación**: http://localhost:8080
- **Admin**: http://localhost:8080/admin

## 📱 Uso del Sistema

### Para Usuarios
- **Registro**: Crear cuenta con email y contraseña
- **Búsqueda**: Buscar anime por título o palabras clave
- **Favoritos**: Marcar contenido de interés
- **Recomendaciones**: Recibir sugerencias personalizadas

### Para Desarrolladores
- **Admin Panel**: Gestión completa de usuarios y favoritos
- **API Ready**: Estructura preparada para múltiples APIs
- **Extensible**: Fácil agregar nuevos tipos de contenido

## 🔧 Comandos Útiles

```bash
# Ver logs de la aplicación
docker-compose logs web

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ejecutar comandos Django
docker-compose run web python manage.py [comando]

# Shell interactivo
docker-compose run web python manage.py shell
```

## 🌟 Roadmap y Expansiones Planificadas

### 📺 Películas y Series
- Integración con TMDB (The Movie Database)
- Búsqueda por género, año, director
- Trailers y información detallada

### 📚 Libros
- Integración con OpenLibrary API
- Búsqueda por autor, género, ISBN
- Reseñas y ratings

### 🎵 Música
- Integración con Spotify API
- Búsqueda de artistas, álbumes, playlists
- Recomendaciones basadas en géneros

### 🧠 IA y Machine Learning
- Análisis de sentimientos en reseñas
- Clustering de usuarios similares
- Algoritmos de recomendación avanzados
- Procesamiento de lenguaje natural para mejores búsquedas

### 📊 Analytics y Métricas
- Dashboard de estadísticas de usuario
- Métricas de popularidad de contenido
- A/B testing para algoritmos de recomendación

## 🛡️ Seguridad y Consideraciones

- Validación de entrada en todos los formularios
- Rate limiting para APIs externas
- Sesiones seguras con timeouts configurables
- Sanitización de datos de APIs externas
- Preparado para HTTPS en producción

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas que Necesitan Contribución
- Implementación de nuevas APIs (TMDB, OpenLibrary, Spotify)
- Mejoras en el algoritmo de recomendaciones
- Tests unitarios y de integración
- Optimización de performance
- UI/UX improvements

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto y Soporte

- **Issues**: Reporta bugs o solicita features en [GitHub Issues](../../issues)
- **Documentación**: Wiki del repositorio para guías detalladas
- **API Docs**: Documentación de endpoints en `/docs/` (próximamente)

---

Sistema desarrollado con ❤️ usando Django, PostgreSQL y Docker. Preparado para escalar a múltiples tipos de contenido multimedia.