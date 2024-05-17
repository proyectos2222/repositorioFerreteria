from django.contrib import admin
from .models import *

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Imagen_producto)
admin.site.register(Pedido)
admin.site.register(Carrito)
admin.site.register(Carrito_item)
admin.site.register(Estado)
admin.site.register(Info_cliente)
admin.site.register(Marca)

