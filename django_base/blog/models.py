# BLOG app models.py
from django.db import models
from django.conf import settings 

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=200, unique=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['name']
        verbose_name = "category"
        verbose_name_plural = "categories"


    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    featured_image = models.URLField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    alt_image = models.TextField(null=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title