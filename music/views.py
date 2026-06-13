import os


from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, HttpResponse, Http404, JsonResponse

from django.contrib.auth.models import User
from .models import Song, UserProfile


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    songs = Song.objects.all()
    return render(request, 'home.html', {'songs': songs})


def search(request):
    if not request.user.is_authenticated:
        return redirect('login')

    query = request.GET.get('q', '')
    songs = Song.objects.filter(title__icontains=query)
    return render(request, 'home.html', {'songs': songs, 'query': query})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            return render(
                request,
                'register.html',
                {'error': 'All fields are required'},
                status=400)

        if len(password) < 8:
            return render(
                request,
                'register.html',
                {'error': 'Password must be at least 8 characters'},
                status=400)

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'register.html',
                {'error': 'Username already exists'},
                status=400)

        if User.objects.filter(email=email).exists():
            return render(
                request,
                'register.html',
                {'error': 'Email already exists'},
                status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        UserProfile.objects.create(user=user)

        return redirect('login')

    return render(request, 'register.html', status=200)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(
                request,
                'login.html',
                {'error': 'All fields are required'},
                status=400)

        if not User.objects.filter(username=username).exists():
            return render(
                request,
                'login.html',
                {'error': 'Username does not exist'},
                status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)

            login(request, user)
            return redirect('home')

        return render(
            request,
            'login.html',
            {'error': 'Invalid credentials'},
            status=400)

    return render(request, 'login.html', status=200)


def logout_view(request):
    logout(request)
    return redirect('login')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = request.user.userprofile

    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('bio')
        image = request.FILES.get('profile_picture')

        if image:
            profile.user_image = image

        if name and name != profile.name:
            profile.name = name

        if username and username != request.user.username:
            request.user.username = username

        profile.save()

        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile}, status=200)


def serve_song(request, song_id):
    if not request.user.is_authenticated:
        raise Http404

    try:
        song = Song.objects.get(pk=song_id)
    except RuntimeError:
        raise Http404

    file_path = os.path.join(settings.MEDIA_ROOT, song.audio_file.name)

    if not os.path.exists(file_path):
        raise Http404

    response = FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
    response['Accept-Ranges'] = 'bytes'

    # Manejar Range request
    range_header = request.META.get('HTTP_RANGE')
    if range_header:
        file_size = os.path.getsize(file_path)
        range_val = range_header.strip().replace('bytes=', '')
        start, end = range_val.split('-')
        start = int(start)
        end = int(end) if end else file_size - 1

        f = open(file_path, 'rb')
        f.seek(start)
        data = f.read(end - start + 1)
        f.close()

        response = HttpResponse(data, status=206, content_type='audio/mpeg')
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = len(data)

    return response
