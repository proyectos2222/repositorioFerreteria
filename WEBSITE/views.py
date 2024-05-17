from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import requests
from .models import *
from django.db.models import Q

# SDK de Mercado Pago (si da problemas, instalar con: pip install mercadopago)
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("TEST-937485966507246-051120-5327fec403daba4a078a7d4a79547a6a-1774376550")


def Base(request):

    if request.user.groups.filter(name="vendedor").exists():
        grupo = "vendedor"
    elif request.user.groups.filter(name="bodeguero").exists():
        grupo = "bodeguero"
    elif request.user.groups.filter(name="contador").exists():
        grupo = "contador"
    else:
        grupo = "cliente"

    usuario = request.user
    carrito = Carrito.objects.filter(estado=False,usuario=usuario).first()
    contador=Carrito_item.objects.filter(id_carrito=carrito).count()

    context = {
        "grupo": grupo,
        "contador":contador
    }

    return render(request,'base.html', context)

# VISTA LOGIN
def Login(request):

    return render(request,'login.html')


def Woi(request):

    return render(request, 'woi.html')


# VISTA LANDING
def Landing(request):

    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        # Manejar el caso del usuario no autenticado
        return redirect('login')  # Redirige al usuario a la página de inicio de sesión
    usuario = request.user
    carrito = Carrito.objects.filter(estado=False,usuario=usuario).first()
    contador=Carrito_item.objects.filter(id_carrito=carrito).count()

    context = {
        "contador" : contador
    }
    return render(request, 'landing.html',context)

# formulario para registrarse
class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
# VISTA REGISTRO
def Register(request):

    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("landing")
    else:
        form = FormularioRegistro()

    return render(request, 'registration/register.html',{"form":form})
    
#VISTA PARA AGREGAR NUEVOS PRODUCTOS
@login_required
def Agregar(request):
    if request.user.groups.filter(name="vendedor").exists():
        grupo = "vendedor"
    elif request.user.groups.filter(name="bodeguero").exists():
        grupo = "bodeguero"
    elif request.user.groups.filter(name="contador").exists():
        grupo = "contador"
    else:
        grupo = "cliente"


    cat = Categoria.objects.raw("select * from website_categoria")
    marcas = Marca.objects.raw("select * from website_marca")

    if request.method == "POST":
        nombre_producto = request.POST["nombre"]
        precio = request.POST["precio"]
        descripcion = request.POST["descripción"]
        categoria = request.POST["categoria"]
        marcaProd = request.POST["marca"]
        objCategoria = Categoria.objects.get(id_categoria=categoria)
        objMarca = Marca.objects.get(id_marca=marcaProd)
        objProducto = Producto.objects.create(
            nombre_producto=nombre_producto,
            precio=precio,
            descripcion=descripcion,
            id_categoria=objCategoria,
            id_marca=objMarca
        )

        imagen = request.FILES.get("imagen")
        Imagen_producto.objects.create(
            imagen_producto=imagen,
            id_producto=objProducto
        )

        context = {
            "mensaje": "Oferta publicada exitosamente",
            "grupo": grupo,
            "cat": cat,
            "marca": marcas
            }
        return render(request, "agregar.html", context)
    else:
        context = {
            "grupo": grupo,
            "cat": cat,
            "marca": marcas
            }
        return render(request, "agregar.html", context)
    
def Editar(request,pk):
    if request.user.groups.filter(name="vendedor").exists():
        grupo = "vendedor"
    elif request.user.groups.filter(name="bodeguero").exists():
        grupo = "bodeguero"
    elif request.user.groups.filter(name="contador").exists():
        grupo = "contador"
    else:
        grupo = "cliente"


    cat = Categoria.objects.raw("select * from website_categoria")

    try:
            producto = Producto.objects.get(id_producto=pk)
            context = {
            "mensaje": "Producto actualizado exitosamente",
            "grupo": grupo,
            "cat": cat,
            "producto": producto,
            }
            return render(request, "editar.html", context)
    except:
            context = {
            "mensaje": "Oferta no encontrada!",
            "grupo": grupo,
            "cat": cat,
            }
            return render(request, "list.html", context)

def Updateproducto(request):
    if request.user.groups.filter(name="vendedor").exists():
        grupo = "vendedor"
    elif request.user.groups.filter(name="bodeguero").exists():
        grupo = "bodeguero"
    elif request.user.groups.filter(name="contador").exists():
        grupo = "contador"
    else:
        grupo = "cliente"


    cat = Categoria.objects.raw("select * from website_categoria")
    if request.method == "POST":
        id_producto = request.POST["id_producto"]
        nombre_producto = request.POST["nombre"]
        precio = request.POST["precio"]
        descripcion = request.POST["descripción"]
        categoria = request.POST["categoria"]
        objCategoria = Categoria.objects.get(id_categoria=categoria)

        objProducto = Producto()
        objProducto.id_producto = id_producto
        objProducto.nombre_producto = nombre_producto
        objProducto.precio = precio
        objProducto.descripcion = descripcion
        objProducto.id_categoria = objCategoria

        imagen = request.FILES.get("imagen")
        Imagen_producto.objects.create(
            imagen_producto=imagen,
            id_producto=objProducto
        )

        context = {
        'mensaje' : "Se guardaron los cambios hechos en la oferta",
        "grupo": grupo,
        }
        return(render(request,'editar.html',context))
    
def Eliminar(request,pk):
    if request.user.groups.filter(name="vendedor").exists():
        grupo = "vendedor"
    elif request.user.groups.filter(name="bodeguero").exists():
        grupo = "bodeguero"
    elif request.user.groups.filter(name="contador").exists():
        grupo = "contador"
    else:
        grupo = "cliente"

    try:
        producto = Producto.objects.get(id_producto=pk)
        producto.delete()
        mensaje = "Producto Eliminado Correctamente"
        context = {
            "mensaje": mensaje,
            "grupo": grupo,
        }
    except:
        mensaje = "Error, el producto no fue encontrado"
        context = {
            "mensaje": mensaje,
            "grupo": grupo,
        }
    return(redirect("list"))

#SOLO PARA EL USUARIO VENDEDOR
@login_required
def Bodega(request):
    if request.user.groups.filter(name="vendedor").exists():
        grupo = "vendedor"
    elif request.user.groups.filter(name="bodeguero").exists():
        grupo = "bodeguero"
    elif request.user.groups.filter(name="contador").exists():
        grupo = "contador"
    else:
        grupo = "cliente"

    producto = Producto.objects.all().order_by('nombre_producto')
    context = {
        'grupo' : grupo,
        'producto' : producto
    }
    return(render(request,'bodega.html',context,))

#LISTADO DE PRODUCTOS 
@login_required
def List(request):
    if request.user.groups.filter(name="vendedor").exists():
        grupo = "vendedor"
    elif request.user.groups.filter(name="bodeguero").exists():
        grupo = "bodeguero"
    elif request.user.groups.filter(name="contador").exists():
        grupo = "contador"
    else:
        grupo = "cliente"
        
    producto = Producto.objects.all().order_by('nombre_producto')
    context = {
        'grupo' : grupo,
        'producto' : producto
    }
    return(render(request,'list.html',context,))

def get_productos():
    url = 'http://localhost/api/api/get.php' 
    r = requests.get(url)
    return r.json()

def Catalogo(request):
    usuario = request.user
    carrito = Carrito.objects.filter(estado=False,usuario=usuario).first()
    contador=Carrito_item.objects.filter(id_carrito=carrito).count()

    productos = Producto.objects.all()
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()

    palabra_clave = request.GET.get('palabra_clave')
    tipo_producto = request.GET.get('tipo_producto')
    marca = request.GET.get('marca')
    precio = request.GET.get('precio')
    stock_disponible = get_productos()
    stock=stock_disponible[0]

    if palabra_clave:
        productos = productos.filter(Q(nombre_producto__icontains=palabra_clave) | Q(descripcion__icontains=palabra_clave))
    if tipo_producto:
        productos = productos.filter(id_categoria=tipo_producto)
    if marca:
        productos = productos.filter(id_marca=marca)
    if precio==1:
        productos = productos.order_by('precio')
    elif precio==2:
        productos = productos.order_by('-precio')

    context = {     
        "productos": productos,
        "marcas": marcas,
        "categorias" : categorias,
        "contador" : contador,
        "stock" : stock
    }   

    return render(request, 'catalogo.html', context)

@login_required
def VerCarrito(request):
    usuario = request.user
    carrito = Carrito.objects.filter(estado=False,usuario=usuario).first()
    carritoItems = Carrito_item.objects.filter(id_carrito = carrito)
    carro = Carrito.objects.filter(usuario=request.user,estado=False).first()
    contCarrito=Carrito_item.objects.filter(id_carrito=carro)
    contador=Carrito_item.objects.filter(id_carrito=carro).count()
    subTotal= sum([item.cantidad* item.id_producto.precio for item in contCarrito])
    total=subTotal+2500

    item = [[9000,'precioenvio','envio',1,2500,"CLP"]]

    for x in carritoItems:
        item.append([x.id_producto.id_producto,x.id_producto.nombre_producto,x.id_producto.descripcion,x.cantidad,x.id_producto.precio,"CLP"])

    items = []

    for x in item:
        items.append({
            "id": x[0],  # El primer elemento de x es el ID del producto
            "title": x[1],  # El segundo elemento de x es el nombre del producto
            "description": x[2],  # El tercer elemento de x es la descripción del producto
            "quantity": x[3],  # El cuarto elemento de x es la cantidad
            "unit_price": x[4],  # El quinto elemento de x es el precio unitario
            "currency_id": x[5]  # El sexto elemento de x es la moneda
        })

    # Creación la preferencia, necesario para Mercado pago
    preference_data = {
        "back_urls": {
            "success": "http://localhost:8000/resultadopago/exito",
            "failure": "http://localhost:8000/resultadopago/fallo",
            "pending": "http://localhost:8000/resultadopago/pendiente"
        }, 
        # En items va la informacion de los productos por lo que se está pagando sta información se saca desde la base de datos 
        "items": items
        # notification_url es para mostrar el resultado de la compra aunque el usuario no vuelva a la página despues de terminar el pago
        # Para probar el notification_url se tiene que usar ngrok
        # "notification_url": "http://localhost:8000/resultadopago/notificacion"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    print(preference)



    context={
        'contCarrito':contCarrito,
        'subTotal':subTotal,
        'total':total,
        'carro':carro,
        'contador':contador,
        'url': preference["init_point"],
    }

    return render(request, 'carrito.html',context )

@login_required
def AñadirCarritoCompra(request):
    if request.method == 'POST':
        usuario=request.user
        id_producto=request.POST['id_producto']
        prod=Producto.objects.filter(id_producto=id_producto).first()
        cantidad=request.POST['cantidad']
        if Carrito.objects.filter(usuario=usuario,estado=False).first() == None:
            Carrito.objects.create(usuario=usuario,estado=False)

        carrito = Carrito.objects.filter(usuario=usuario,estado=False).first()
        if Carrito_item.objects.filter(id_carrito=carrito,id_producto=prod).first():
            carrito_item=Carrito_item.objects.filter(id_carrito=carrito,id_producto=id_producto).first()
            carrito_item.cantidad+=int(cantidad)
            carrito_item.save()
            messages.success(request,'Agregado correctamente')
            return redirect('catalogo')
        else:
            Carrito_item.objects.create(id_carrito=carrito,id_producto=prod,cantidad=cantidad)
            messages.success(request,'Agregado correctamente')
            return redirect('catalogo')

    return render(request,'catalogo.html') 

@login_required
def ActualizarCantidadCarrito(request):
    if request.method=='POST':
        usuario=request.user
        car= request.POST.get('id_carrito')
        cantidad= request.POST.get('cantidad')
        prod = request.POST.get('id_producto')
        carItem=Carrito_item.objects.filter(id_carrito=car,id_producto=prod).first()
        carItem.cantidad=cantidad
        carItem.save()
        return redirect('VerCarrito')
    return render(request,'mainCarrito.html')

@login_required
def QuitarCarritoCompra(request):
    if request.method == 'POST':
        usuario=request.user
        carrito = Carrito.objects.filter(usuario=usuario,estado=False)
        if request.POST.get('borrarUno'):
            id_producto=request.POST['id_producto']
            id_carrito=request.POST['id_carrito']
            carrito_item = Carrito_item.objects.filter(id_carrito=id_carrito,id_producto=id_producto)
            carrito_item.delete()
            messages.success(request,'Eliminado correctamente')
            return redirect('VerCarrito')        
        elif request.POST.get('borrarTodo'):
            carrito.delete()
            Carrito.objects.create(estado=False,usuario=usuario)
            messages.success(request,'Eliminado Correctamente')
            return redirect('VerCarrito')
    return render(request,'mainCarrito.html')

def ResultadoPago(request,rp):
    context={
        'rp':rp
    }

    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario,estado=False)

    if rp == "exito":
        carrito.estado=True

    return render(request, 'resultadopago.html',context)

def Detalle(request,id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    usuario = request.user
    carrito = Carrito.objects.filter(estado=False,usuario=usuario).first()
    contador=Carrito_item.objects.filter(id_carrito=carrito).count()


    context= {
        'producto':producto,
        'contador':contador
    }

    return render(request, 'detalle.html',context)