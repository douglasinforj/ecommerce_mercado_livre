import django_filters
from .models import Product, Category, Brand

class ProductFilter(django_filters.FilterSet):
    """Filtros avançados para produtos"""
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nome')
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.filter(is_active=True),
        widget=django_filters.widgets.SelectMultiple,
        label='Categorias'
    )
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.filter(is_active=True),
        widget=django_filters.widgets.SelectMultiple,
        label='Marcas'
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Preço mínimo')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Preço máximo')
    
    # Ordenação
    o = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('-price', 'price_desc'),
            ('name', 'name'),
            ('-created_at', 'newest'),
        ),
        field_labels={
            'price': 'Menor preço',
            'price_desc': 'Maior preço',
            'name': 'Nome (A-Z)',
            'newest': 'Mais recentes',
        }
    )
    
    class Meta:
        model = Product
        fields = ['category', 'brand', 'is_featured']