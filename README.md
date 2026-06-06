# FlowMusic

Un reproductor de música online multiplataforma construido con Django 5.x.

## Características

- Backend: Django 5.x
- Frontend: HTML5/CSS3 con Bootstrap
- Base de datos: SQLite
- Reproducción de audio con HTML5 <audio>
- Búsqueda de canciones
- Panel de administración para subir canciones
- Playlists de usuario

## Instalación

1. Clona o descarga el proyecto.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta las migraciones: `python manage.py migrate`
4. Crea un superusuario: `python manage.py createsuperuser`
5. Ejecuta el servidor: `python manage.py runserver`

## Uso

- Accede a la aplicación en http://localhost:8000
- Usa el panel de admin en http://localhost:8000/admin para subir artistas, álbumes y canciones.
- Busca canciones en la barra de búsqueda.
- Haz clic en "Reproducir" para escuchar una canción.

## Estructura de Modelos

- **Artist**: Nombre, biografía, imagen
- **Album**: Título, portada, artista
- **Song**: Título, archivo de audio, duración, álbum
- **Playlist**: Usuario, canción (para playlists personales)