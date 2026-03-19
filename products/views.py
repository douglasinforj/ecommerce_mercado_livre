from django.shortcuts import render, get_object_or_404

from .models import Product, Category

from .filters import ProductFilter
from django.core.paginator import Paginator

from django.db.models import Q, Count



def home(request):
    #Pagina inicial com destaques e novidades
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]    #slice limite de 8
    new_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)



def product_list(request):
    """Lista todos os produtos com filtros"""
    products = Product.objects.filter(is_available=True)
    
    # Aplicar filtros
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    
    # Paginação
    paginator = Paginator(products, 12)  # 12 produtos por página
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    # Categorias para o menu
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'filter': product_filter,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Detalhes do produto"""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Incrementar contador de visualizações
    product.views_count += 1
    product.save(update_fields=['views_count'])
    
    # Produtos relacionados (mesma categoria)
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def category_products(request, slug):
    """Produtos por categoria"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_available=True)
    
    # Paginação
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_products.html', context)


def search(request):
    """Busca de produtos"""
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(sku__icontains=query),
            is_available=True
        ).distinct()
    else:
        products = Product.objects.none()
    
    # Paginação
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'query': query,
        'total_results': products.paginator.count if products else 0,
    }
    return render(request, 'products/search.html', context)

    