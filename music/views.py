from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import Song


def home(request):
    songs = Song.objects.all()
    return render(request, 'home.html', {'songs': songs})


def search(request):
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

        return redirect('home')

    return render(request, 'register.html', status=200)
