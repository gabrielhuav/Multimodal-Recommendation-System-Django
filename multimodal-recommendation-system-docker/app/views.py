from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario, Favorito
from .forms import UsuarioForm, LoginForm, AnimeSearchForm, LibroSearchForm
from django.utils.translation import activate
from django.utils import translation
import requests
import time # Added for rate limiting in recommendations

def index(request):
    user_info = ""
    if 'usuario_id' in request.session:
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            user_info = f"<p>Bienvenido, {usuario.nombre}! (<a href='/logout/'>Cerrar sesión</a>)</p>"
            # Adding links for new features if user is logged in
            user_info += "<p><a href='/buscar-anime/'>Buscar Anime</a> | <a href='/buscar-libros/'>Buscar Libros</a> | <a href='/mis-favoritos/'>Mis Favoritos</a> | <a href='/recomendaciones/'>Recomendaciones Anime</a> | <a href='/recomendaciones-libros/'>Recomendaciones Libros</a></p>"
        except Usuario.DoesNotExist:
            request.session.flush() # Clear session if user ID is invalid
            user_info = "<p><a href='/login/'>Iniciar sesión</a> | <a href='/registro/'>Registrarse</a></p>"
    else:
        user_info = "<p><a href='/login/'>Iniciar sesión</a> | <a href='/registro/'>Registrarse</a></p>"
    
    return HttpResponse(f"<h1>¡Hola, Django desde Docker!</h1>{user_info}<br><a href='/usuarios/'>Ver usuarios (requiere login)</a>")

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario registrado exitosamente!')
            return redirect('login_usuario') # Redirect to login after successful registration
    else:
        form = UsuarioForm()
    
    return render(request, 'registro.html', {'form': form})

def lista_usuarios(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver la lista de usuarios.')
        return redirect('login_usuario')
    
    try:
        # Ensure the logged-in user exists
        Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida o ha expirado. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')
    
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_rol'] = usuario.rol
            messages.success(request, f'¡Bienvenido de nuevo, {usuario.nombre}!')
            # Redirect to a more relevant page, e.g., dashboard or anime search
            return redirect('buscar_anime') 
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_usuario(request):
    request.session.flush()
    messages.success(request, '¡Sesión cerrada exitosamente!')
    return redirect('index')

def buscar_anime(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para buscar anime.')
        return redirect('login_usuario')

    try:
        current_user = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')

    form = AnimeSearchForm()
    resultados_api = None
    error_api = None
    
    favoritos_ids = list(Favorito.objects.filter(usuario=current_user, tipo_contenido='anime').values_list('contenido_id', flat=True))

    if request.method == 'GET' and 'query' in request.GET:
        form = AnimeSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                # Using sfw filter to ensure content is generally safe for work
                response = requests.get(f"https://api.jikan.moe/v4/anime?q={query}&sfw")
                response.raise_for_status() 
                resultados_api = response.json().get('data', [])
            except requests.exceptions.RequestException as e:
                error_api = f"Error al contactar la API de Jikan: {e}"
            except ValueError: 
                error_api = "Error al procesar la respuesta de la API de Jikan."
    
    resultados_procesados = []
    if resultados_api:
        for anime_data in resultados_api:
            mal_id = anime_data.get('mal_id')
            if isinstance(mal_id, int):
                anime_data['es_favorito'] = str(mal_id) in favoritos_ids
            else:
                anime_data['es_favorito'] = False 
            resultados_procesados.append(anime_data)

    return render(request, 'anime_search.html', {
        'form': form,
        'resultados': resultados_procesados,
        'error_api': error_api
    })

def toggle_favorito(request):
    if 'usuario_id' not in request.session:
        messages.error(request, 'Debes iniciar sesión para gestionar tus favoritos.')
        return redirect(request.META.get('HTTP_REFERER', 'login_usuario'))

    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect(request.META.get('HTTP_REFERER', 'login_usuario'))

    if request.method == 'POST':
        contenido_id = request.POST.get('contenido_id') or request.POST.get('anime_id')
        contenido_titulo = request.POST.get('contenido_titulo') or request.POST.get('anime_titulo')
        tipo_contenido = request.POST.get('tipo_contenido', 'anime')
        autor = request.POST.get('autor', '')

        if not contenido_id or not contenido_titulo:
            messages.error(request, 'Datos incompletos para marcar como favorito.')
            return redirect(request.META.get('HTTP_REFERER', 'buscar_anime'))

        try:
            favorito_existente, created = Favorito.objects.get_or_create(
                usuario=usuario,
                contenido_id=str(contenido_id),
                tipo_contenido=tipo_contenido,
                defaults={
                    'contenido_titulo': contenido_titulo,
                    'autor': autor if tipo_contenido == 'libro' else None
                }
            )
            
            if created:
                messages.success(request, f'"{contenido_titulo}" añadido a tus favoritos.')
            else:
                favorito_existente.delete()
                messages.info(request, f'"{contenido_titulo}" eliminado de tus favoritos.')
                
        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar tu solicitud: {str(e)}')
            
        return redirect(request.META.get('HTTP_REFERER', 'buscar_anime'))

    return redirect(request.META.get('HTTP_REFERER', 'buscar_anime'))

def mis_favoritos(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver tus favoritos.')
        return redirect('login_usuario')
    try:
        current_user = Usuario.objects.get(id=request.session['usuario_id'])
        favoritos = Favorito.objects.filter(usuario=current_user).order_by('-fecha_agregado')
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')
    
    return render(request, 'mis_favoritos.html', {'favoritos': favoritos})

def recomendaciones_anime(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver recomendaciones.')
        return redirect('login_usuario')

    try:
        current_user = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')

    user_favoritos = Favorito.objects.filter(usuario=current_user, tipo_contenido='anime')
    if not user_favoritos:
        messages.info(request, 'Añade algunos animes a tus favoritos para obtener recomendaciones.')
        return render(request, 'recomendaciones_anime.html', {'recomendaciones': []})

    recomendaciones_dict = {}
    error_api = None
    
    favoritos_ids = list(user_favoritos.values_list('contenido_id', flat=True))

    for i, favorito in enumerate(user_favoritos):
        anime_id = favorito.contenido_id
        try:
            if i > 0: 
                time.sleep(0.4) # Jikan API rate limit: ~3 req/sec. Be considerate.

            response = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations")
            response.raise_for_status()
            data = response.json().get('data', [])
            
            for rec_item in data:
                anime_entry = rec_item.get('entry')
                if anime_entry and anime_entry.get('mal_id'):
                    mal_id = anime_entry['mal_id']
                    if mal_id not in favoritos_ids and mal_id not in recomendaciones_dict:
                        anime_entry['es_favorito'] = False # By definition, these are not yet favorites
                        recomendaciones_dict[mal_id] = anime_entry
        
        except requests.exceptions.RequestException as e:
            error_api = f"Error al obtener recomendaciones de la API de Jikan: {e}. Algunas recomendaciones podrían faltar."
            break 
        except ValueError:
            error_api = "Error al procesar la respuesta de la API de Jikan para recomendaciones."
            break

    recomendaciones_list = list(recomendaciones_dict.values())
    
    # Shuffle recommendations for variety if desired, e.g. import random; random.shuffle(recomendaciones_list)

    return render(request, 'recomendaciones_anime.html', {
        'recomendaciones': recomendaciones_list,
        'error_api': error_api
    })

def buscar_libros(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para buscar libros.')
        return redirect('login_usuario')

    try:
        current_user = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')

    form = LibroSearchForm()
    resultados_api = None
    error_api = None
    
    favoritos_ids = list(Favorito.objects.filter(usuario=current_user, tipo_contenido='libro').values_list('contenido_id', flat=True))

    if request.method == 'GET' and 'query' in request.GET:
        form = LibroSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                response = requests.get(f"https://openlibrary.org/search.json?q={query}&limit=20")
                response.raise_for_status() 
                resultados_api = response.json().get('docs', [])
            except requests.exceptions.RequestException as e:
                error_api = f"Error al contactar la API de OpenLibrary: {e}"
            except ValueError: 
                error_api = "Error al procesar la respuesta de la API de OpenLibrary."
    
    resultados_procesados = []
    if resultados_api:
        for libro_data in resultados_api:
            # Extraer información del libro
            work_key = libro_data.get('key', '')
            if work_key:
                libro_data['work_id'] = work_key.split('/')[-1]
                libro_data['es_favorito'] = libro_data['work_id'] in favoritos_ids
                
                # Procesar datos adicionales
                libro_data['author_name'] = ', '.join(libro_data.get('author_name', ['Autor desconocido']))
                libro_data['first_publish_year'] = libro_data.get('first_publish_year', 'N/A')
                
                # URL de la imagen del libro
                if 'cover_i' in libro_data:
                    libro_data['cover_url'] = f"https://covers.openlibrary.org/b/id/{libro_data['cover_i']}-M.jpg"
                else:
                    libro_data['cover_url'] = None
                    
                resultados_procesados.append(libro_data)

    return render(request, 'libro_search.html', {
        'form': form,
        'resultados': resultados_procesados,
        'error_api': error_api
    })

def recomendaciones_libros(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver recomendaciones.')
        return redirect('login_usuario')

    try:
        current_user = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')

    user_favoritos_libros = Favorito.objects.filter(usuario=current_user, tipo_contenido='libro')
    if not user_favoritos_libros:
        messages.info(request, 'Añade algunos libros a tus favoritos para obtener recomendaciones.')
        return render(request, 'recomendaciones_libros.html', {'recomendaciones': []})

    recomendaciones_list = []
    error_api = None
    
    favoritos_ids = list(user_favoritos_libros.values_list('contenido_id', flat=True))

    # Buscar libros similares basados en los autores de libros favoritos
    try:
        for favorito in user_favoritos_libros[:3]:  # Limitamos a 3 favoritos para no saturar la API
            # Obtener el autor del libro favorito
            autor_busqueda = favorito.autor
            if autor_busqueda and autor_busqueda != 'Autor desconocido':
                # Buscar más libros del mismo autor
                response = requests.get(f"https://openlibrary.org/search.json?author={autor_busqueda}&limit=5")
                response.raise_for_status()
                data = response.json().get('docs', [])
                
                for libro_data in data:
                    work_key = libro_data.get('key', '')
                    if work_key:
                        work_id = work_key.split('/')[-1]
                        # No recomendar libros que ya están en favoritos
                        if work_id not in favoritos_ids:
                            libro_data['work_id'] = work_id
                            libro_data['es_favorito'] = False
                            libro_data['author_name'] = ', '.join(libro_data.get('author_name', ['Autor desconocido']))
                            libro_data['first_publish_year'] = libro_data.get('first_publish_year', 'N/A')
                            
                            if 'cover_i' in libro_data:
                                libro_data['cover_url'] = f"https://covers.openlibrary.org/b/id/{libro_data['cover_i']}-M.jpg"
                            else:
                                libro_data['cover_url'] = None
                                
                            recomendaciones_list.append(libro_data)
            
            time.sleep(0.5)  # Rate limiting para OpenLibrary
            
    except requests.exceptions.RequestException as e:
        error_api = f"Error al obtener recomendaciones de la API de OpenLibrary: {e}"
    except ValueError:
        error_api = "Error al procesar la respuesta de la API de OpenLibrary."

    # Eliminar duplicados y limitar resultados
    seen_ids = set()
    recomendaciones_unicas = []
    for libro in recomendaciones_list:
        if libro['work_id'] not in seen_ids:
            seen_ids.add(libro['work_id'])
            recomendaciones_unicas.append(libro)
            if len(recomendaciones_unicas) >= 12:  # Limitar a 12 recomendaciones
                break

    return render(request, 'recomendaciones_libros.html', {
        'recomendaciones': recomendaciones_unicas,
        'error_api': error_api
    })

def cambiar_idioma(request):
    """Vista personalizada para cambiar el idioma"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            # Activar el idioma en la sesión
            translation.activate(language)
            request.session['django_language'] = language
            
            # Obtener la URL de redirección
            next_page = request.POST.get('next', '/')
            
            # Asegurar que la redirección sea segura
            if not next_page or next_page.startswith('/i18n/'):
                next_page = '/'
                
            return redirect(next_page)
    
    return redirect('/')