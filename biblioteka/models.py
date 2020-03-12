# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    publishingHouse = models.CharField(max_length=200)
    description = models.TextField()
    numberOfPages = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    bookCondition = models.CharField(max_length=100)
    image = models.TextField()
    idKey = models.SmallIntegerField()

    def add(self):
        self.save()

    def __str__(self):
        return self.title
