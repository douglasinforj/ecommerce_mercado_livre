from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'get_total']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'get_total_items', 'get_total', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'session_key']
    readonly_fields = ['created_at', 'updated_at', 'get_total']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Itens'
    
    def get_total(self, obj):
        return f'R$ {obj.get_total()}'
    get_total.short_description = 'Total'

admin.site.register(Cart, CartAdmin)