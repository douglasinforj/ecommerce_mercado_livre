# orders/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'quantity', 'price', 'total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'get_status_badge', 'total', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email', 'customer_cpf']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'paid_at']
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('order_number', 'user', 'cart', 'status', 'payment_method', 'payment_id')
        }),
        ('Valores', {
            'fields': ('subtotal', 'shipping_cost', 'discount', 'total')
        }),
        ('Dados do Cliente', {
            'fields': ('customer_name', 'customer_email', 'customer_cpf', 'shipping_phone')
        }),
        ('Endereço de Entrega', {
            'fields': ('shipping_address', ('shipping_city', 'shipping_state'), 'shipping_zipcode')
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at', 'paid_at')
        }),
    )
    
    inlines = [OrderItemInline]
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_delivered']
    
    def get_status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'blue',
            'processing': 'purple',
            'shipped': 'teal',
            'delivered': 'green',
            'cancelled': 'red',
            'refunded': 'gray',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    get_status_badge.short_description = 'Status'
    
    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_as_paid.short_description = 'Marcar como pago'
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'Marcar como enviado'
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Marcar como entregue'