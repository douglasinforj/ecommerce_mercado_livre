from django.shortcuts import render

from .models import Product, Category


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





    