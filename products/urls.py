from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.product_list, name='product_list'),
    path('produto/<slug:slug>/', views.product_detail, name='detail'),
    path('categoria/<slug:slug>/', views.category_products, name='category'),
    path('busca/', views.search, name='search'),
]