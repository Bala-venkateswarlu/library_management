from django.db import models

# Create your models here.

class Library(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    reference_id = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    adress = models.CharField(max_length=100)
    password = models.CharField(max_length=20, default='Unknown')

class Books(models.Model):
    book_name = models.CharField(max_length=100)
    Author = models.CharField(max_length=50)
    published = models.TextField()


class Reader(models.Model):
    reader_name = models.CharField(max_length=100)
    reference_id = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    Author = models.CharField(max_length=50, default='Unknown Author')  
    published = models.TextField(default='Unknown Date')  
    start_date = models.DateField()
    end_date = models.DateField()
    