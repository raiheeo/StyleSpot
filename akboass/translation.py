from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Support, User, Cart, CartItem


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'color', 'material')


