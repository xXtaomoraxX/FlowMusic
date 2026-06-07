from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .models import Song


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

    return render(request, 'profile.html', status=200)
