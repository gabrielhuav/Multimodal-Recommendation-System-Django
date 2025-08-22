from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario, Favorito
from .forms import UsuarioForm, LoginForm, AnimeSearchForm
import requests
import time # Added for rate limiting in recommendations

def index(request):
    user_info = ""
    if 'usuario_id' in request.session:
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            user_info = f"<p>Bienvenido, {usuario.nombre}! (<a href='/logout/'>Cerrar sesión</a>)</p>"
            # Adding links for new features if user is logged in
            user_info += "<p><a href='/buscar-anime/'>Buscar Anime</a> | <a href='/mis-favoritos/'>Mis Favoritos</a> | <a href='/recomendaciones/'>Recomendaciones</a></p>"
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
    
    favoritos_ids = list(Favorito.objects.filter(usuario=current_user).values_list('anime_id', flat=True))

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
                anime_data['es_favorito'] = mal_id in favoritos_ids
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
        anime_id_str = request.POST.get('anime_id')
        anime_titulo = request.POST.get('anime_titulo')

        if not anime_id_str or not anime_titulo:
            messages.error(request, 'Datos incompletos para marcar como favorito.')
            return redirect(request.META.get('HTTP_REFERER', 'buscar_anime'))

        try:
            anime_id = int(anime_id_str)
            
            favorito_existente, created = Favorito.objects.get_or_create(
                usuario=usuario,
                anime_id=anime_id,
                defaults={'anime_titulo': anime_titulo}
            )
            
            if created:
                messages.success(request, f'"{anime_titulo}" añadido a tus favoritos.')
            else:
                favorito_existente.delete()
                messages.info(request, f'"{anime_titulo}" eliminado de tus favoritos.')
                
        except ValueError:
            messages.error(request, 'ID de anime inválido.')
        except Exception as e: # Catching generic exception for safety
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

    user_favoritos = Favorito.objects.filter(usuario=current_user)
    if not user_favoritos:
        messages.info(request, 'Añade algunos animes a tus favoritos para obtener recomendaciones.')
        return render(request, 'recomendaciones_anime.html', {'recomendaciones': []})

    recomendaciones_dict = {}
    error_api = None
    
    favoritos_ids = list(user_favoritos.values_list('anime_id', flat=True))

    for i, favorito in enumerate(user_favoritos):
        anime_id = favorito.anime_id
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