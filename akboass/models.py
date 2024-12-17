from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    nickname = models.CharField(max_length=32, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region='KZ')
    user_image = models.ImageField(upload_to='user_image/')
   
    def __str__(self):
        return f' Profile {self.nickname} and {self.email}'

class Category(models.Model):
    category_name = models.TextField(max_length=32, null=False, blank=False)
    sale = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.category_name} (Sale: {"Yes" if self.sale else "No"})'

class Support(models.Model):
    name = models.TextField(max_length=32, null=False, blank=False)
    email = models.TextField(max_length=32, null=False, blank=False)
    phone_number = PhoneNumberField(null=True, blank=True, region='KZ')
    comment = models.TextField(max_length=256, null=False, blank=False)
    comment_image = models.ImageField(upload_to='customer_issue/', null=True, blank=True)
    created_date_support = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'Its {self.name} and customer has problems: {self.comment}'


class Product(models.Model):
    title = models.TextField(max_length=32, null=False, blank=False)
    product_image = models.ImageField(upload_to='product_image/', null=False, blank=False)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    size = models.TextField(max_length=5, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=96, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name='products')
    quantity = models.PositiveSmallIntegerField(verbose_name='quantity-of-product')
    color = models.TextField(max_length=64, null=True, blank=True)
    material = models.TextField(max_length=90, null=False, blank=False)
    stock = models.IntegerField(verbose_name='quantity')
    created_date_product = models.DateField(auto_now_add=True, verbose_name='created_date')

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_date_product']
    
    def __str__(self):
        return f'{self.title} and {self.price}'
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
