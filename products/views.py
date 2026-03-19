from django.shortcuts import render

from .models import Product, Category

from .filters import ProductFilter
from django.core.paginator import Paginator



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





    