from django.db import models

from django.contrib.auth import get_user_model

from cart.models import Cart
from products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Aguardando pagamento'),
        ('paid', 'Pago'),
        ('processing', 'Em preparação'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    )

    PAYMENT_METHODS = (
        ('credit_card', 'Cartão de crédito'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
        ('mercado_pago', 'Mercado Pago'),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, null=True)

    order_number = models.CharField('Número do pedido', max_length=20, unique=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField('Método de pagamento', max_length=20, choices=PAYMENT_METHODS)
    payment_id = models.CharField('ID do pagamento', max_length=100, blank=True)

    # Valores
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField('Frete', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Desconto', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2)

    # Dados de entrega
    shipping_address = models.TextField('Endereço de entrega')
    shipping_city = models.CharField('Cidade', max_length=100)
    shipping_state = models.CharField('Estado', max_length=2)
    shipping_zipcode = models.CharField('CEP', max_length=9)
    shipping_phone = models.CharField('Telefone', max_length=15)

    # Dados do cliente
    customer_name = models.CharField('Nome completo', max_length=200)
    customer_email = models.EmailField('E-mail')
    customer_cpf = models.CharField('CPF', max_length=14)

    notes = models.TextField('Observações', blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    paid_at = models.DateTimeField('Pago em', null=True, blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Gerar número do pedido
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_number[3:])
                self.order_number = f"ORD{str(last_number + 1).zfill(6)}"
            else:
                self.order_number = "ORD000001"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField('Nome do produto', max_length=200)
    product_sku = models.CharField('SKU', max_length=50)
    quantity = models.PositiveIntegerField('Quantidade')
    price = models.DecimalField('Preço unitário', max_digits=10, decimal_places=2)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

