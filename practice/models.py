from django.db import models


# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Singer(models.Model):
    name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE,related_name='singer')

    def __str__(self):
        return self.name


