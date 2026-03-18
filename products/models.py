from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Descrição', blank=True)
    image = models.ImageField('Imagem', upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("products:category", args=[self.slug])
    


class Brand(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    logo = models.ImageField('Logo', upload_to='brands/', blank=True, null=True)
    description = models.TextField('Descrição', blank=True)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.name

