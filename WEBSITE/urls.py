from django.urls import path
from .views import * # no olvidar agregar msg para las notificaciones despues
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('base',Base,name='base'), 
    path('woi',Woi,name='woi'), 
    path('accounts/register',Register,name='register'),
    path('',Landing,name='landing'),
    path('agregar/', Agregar, name='agregar'),
    path('editar/<int:pk>', Editar, name='editar'),
    path('update_producto/', Updateproducto, name='update_producto'),
    path('eliminar/<int:pk>', Eliminar, name='eliminar'),
    path('bodega/', Bodega, name='bodega'),
    path('list/', List, name='list'),
    path('catalogo/', Catalogo, name='catalogo'),
    path('catalogo/<int:id_producto>', Detalle, name='Detalle'),
    path('carrito/',VerCarrito,name='VerCarrito'),
    path('carrito/add',AñadirCarritoCompra,name='AñadirCarritoCompra'),
    path('carrito/upd',ActualizarCantidadCarrito, name="ActualizarCantidadCarrito"),
    path('carrito/del',QuitarCarritoCompra,name='QuitarCarritoCompra'),
    path('resultadopago/<str:rp>',ResultadoPago,name='Resultadopago'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
