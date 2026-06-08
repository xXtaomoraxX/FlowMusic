from os import name

from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='albums/', blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

class Song(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='songs/')
    duration = models.DurationField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.album.artist.name}"

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='My Playlist')  # or something

    class Meta:
        unique_together = ('user', 'song', 'name')  # to avoid duplicates

    def __str__(self):
        return f"{self.user.username}'s {self.name}: {self.song.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user_images/', blank=True)

    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
