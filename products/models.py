from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField     #armazenar textos ricos, ou seja, textos formatados com HTML
import os


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
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Categoria')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name='Marca', null=True, blank=True)
    
    name = models.CharField('Nome', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    sku = models.CharField('SKU', max_length=50, unique=True)
    
    short_description = models.CharField('Descrição curta', max_length=200)
    full_description = RichTextField('Descrição completa')
    specifications = models.JSONField('Especificações', default=dict, blank=True)
    
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    discount_price = models.DecimalField('Preço com desconto', max_digits=10, decimal_places=2, blank=True, null=True)
    
    stock = models.PositiveIntegerField('Estoque', default=0)
    is_available = models.BooleanField('Disponível', default=True)
    is_featured = models.BooleanField('Destaque', default=False)
    
    views_count = models.PositiveIntegerField('Visualizações', default=0)
    
    meta_title = models.CharField('Meta Título', max_length=60, blank=True)
    meta_description = models.CharField('Meta Descrição', max_length=160, blank=True)
    meta_keywords = models.CharField('Meta Palavras-chave', max_length=255, blank=True)
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['is_available', 'is_featured']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])
    
    def get_price(self):
        #Retornar o preço atual (com o desconto se disponível)
        return self.discount_price if self.discount_price else self.price
    
    def get_discount_percentage(self):
        #Calcula porcentagem de desconto
        if self.discount_price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount)
        return 0
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagem', upload_to='products/%Y/%m/')
    alt_text = models.CharField('Texto alternativo', max_length=200, blank=True)
    is_main = models.BooleanField('Principal', default=False)
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Image do Produto'
        verbose_name_plural = 'Imagens do Produto'
        ordering = ['order']

    def __str__(self):
        return f"Image de {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_main:
            # Garantir que apenas uma imagem seja principal
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.image.name) #isola o ultimo componente de um caminho, ignorando o diretorio






