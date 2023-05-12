from django.db import models
from category.models import Category
from autoslug import AutoSlugField


class Book(models.Model):
    # title = models.CharField(max_length=150,unique=True)
    slug = AutoSlugField(unique=True, populate_from='title')
    #image = models.ImageField(upload_to="images/books_img/")
    #author = models.CharField(max_length=200,blank=True)
    #description = models.TextField(max_length=3000,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
   # price = models.IntegerField(blank=False)
    stocks = models.IntegerField(default=20)
    stocks_available = models.BooleanField(default=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    #currency = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField()
    cover_image_url = models.URLField(null=True, blank=True)


    def __str__(self):
      return self.title


