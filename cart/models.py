from django.db import models
from django.contrib.auth import get_user_model


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