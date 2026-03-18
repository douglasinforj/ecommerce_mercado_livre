from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductVariant
from django.utils.html import format_html



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'alt_text', 'is_main', 'order']

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'get_price_display', 'stock', 'is_available', 'is_featured', 'created_at']
    list_filter = ['category', 'brand', 'is_available', 'is_featured']
    search_fields = ['name', 'sku', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'get_product_images']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('category', 'brand', 'name', 'slug', 'sku')
        }),
        ('Descrição', {
            'fields': ('short_description', 'full_description', 'specifications')
        }),
        ('Preços', {
            'fields': ('price', 'discount_price')
        }),
        ('Estoque', {
            'fields': ('stock', 'is_available', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProductImageInline, ProductVariantInline]
    
    def get_price_display(self, obj):
        if obj.discount_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">R$ {}</span> '
                '<span style="color: green; font-weight: bold;">R$ {}</span>',
                obj.price, obj.discount_price
            )
        return f'R$ {obj.price}'
    get_price_display.short_description = 'Preço'
    
    def get_product_images(self, obj):
        images = obj.images.all()
        html = ''
        for img in images[:5]:
            html += f'<img src="{img.image.url}" style="max-height: 50px; margin-right: 5px;" />'
        return format_html(html)
    get_product_images.short_description = 'Imagens'


