from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='uploads/%Y-%m-%d')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
