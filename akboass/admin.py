from django.contrib import admin
from .models import Category, Product, Support, User, Cart, CartItem
from modeltranslation.admin import TranslationAdmin


admin.site.register(Category)
admin.site.register(Support)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(CartItem)


@admin.register(Product)
class ProductAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
