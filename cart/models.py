from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, ProductVariant


User = get_user_model()   #retorna o modelo definido no seu settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return f"Carrinho {self.id} - {self.user or self.session_key}"

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço no momento da adição
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = ['cart', 'product', 'variant']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_total(self):
        return self.price * self.quantity