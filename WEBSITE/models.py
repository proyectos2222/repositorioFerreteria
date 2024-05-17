from django.db import models
from django.contrib.auth.models import User
# CATEGORIA DEL PRODUCTO
class Categoria(models.Model):
    id_categoria = models.AutoField(db_column="id_categoria", primary_key=True)
    nombre_categoria = models.CharField(max_length=45)

    def __str__(self):
        return str(self.nombre_categoria)   

class Marca(models.Model):
    id_marca = models.AutoField(db_column="id_marca", primary_key=True)
    nombre_marca = models.CharField(max_length=45)
    

    def __str__(self):
        return str(self.nombre_marca)

 #Producto
class Producto(models.Model):
    id_producto = models.AutoField(db_column="id_producto", primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=400)
    cant_inventario = models.IntegerField(default=0)
    id_categoria = models.ForeignKey(
        "Categoria", on_delete=models.CASCADE, db_column="id_categoria"
    )
    id_marca = models.ForeignKey(
        "Marca", on_delete=models.CASCADE, db_column="id_marca"
    )

    def __str__(self):
        return str(self.nombre_producto)
    
class Imagen_producto(models.Model):
    id_imagen_p = models.AutoField(db_column="id_imagen_p", primary_key=True)
    imagen_producto = models.FileField(upload_to="productos/", null=True)
    id_producto = models.ForeignKey(
        "Producto", on_delete=models.CASCADE, db_column="id_producto"
    )

    def __str__(self):
        return str(self.id_imagen_p)

class Estado(models.Model):
    id_estado = models.AutoField(db_column='id_envio', primary_key=True, default=None)
    nombre = models.CharField(max_length=100, null=False, default='Pendiente')

    def __str__(self):
        return self.nombre

class Info_cliente(models.Model):
    id_info = models.AutoField(db_column="id_info", primary_key=True)
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    rut = models.CharField(max_length=15)
    direccion = models.CharField(max_length=80)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='usuario', null=True)

class Pedido(models.Model):
    id_pedido = models.AutoField(db_column='id_pedido', primary_key=True, default=None)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='usuario', null=True)
    fecha = models.DateField(auto_now_add=True)
    id_envio = models.ForeignKey('Estado', on_delete=models.CASCADE, db_column='id_envio')
    id_carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE, db_column='id_carrito', default=None)
    
    def __str__(self):
        return str(self.fecha)

    @property
    def total(self):
        carrito_cont = Carrito_item.objects.filter(id_carrito=self.id_carrito)
        subTotal= sum([item.cantidad* item.id_producto.precio for item in carrito_cont])
        return subTotal

    @property
    def items(self):
        carrito_cont = Carrito_item.objects.filter(id_carrito=self.id_carrito)
        return carrito_cont

class Carrito(models.Model):
    id_carrito = models.AutoField(db_column='id_carrito',primary_key=True,default=None)
    estado = models.IntegerField(default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='usuario', null=True)

class Carrito_item(models.Model):
    id_carrito= models.ForeignKey('Carrito', on_delete=models.CASCADE, db_column='id_carrito',default=None)
    id_producto= models.ForeignKey('Producto', on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.IntegerField(default=0,null=True,blank=False)
    @property
    def sub_total(self):
        sub_total=self.cantidad * self.id_producto.precio
        return sub_total
    