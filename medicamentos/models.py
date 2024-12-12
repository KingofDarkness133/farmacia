from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.text import slugify

# Modelo personalizado de usuario
class User(AbstractUser):
    CLIENTE = 'cliente'
    ADMINISTRADOR = 'administrador'
    ROLE_CHOICES = [
        (CLIENTE, 'Cliente'),
        (ADMINISTRADOR, 'Administrador'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CLIENTE,
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return self.username


# Modelo de medicamentos
class Medicamento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

        


# Modelo de carrito


# Modelo de proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    contacto = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    producto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo de ventas
class Venta(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    fecha = models.DateField()

# Señal para crear grupos y asignar permisos
@receiver(post_migrate)
def crear_grupos_y_permisos(sender, **kwargs):
    # Crear grupos
    grupo_cliente, _ = Group.objects.get_or_create(name='Clientes')
    grupo_administrador, _ = Group.objects.get_or_create(name='Administradores')

    # Asignar permisos a administradores
    permisos_administrador = Permission.objects.filter(
        codename__in=['add_medicamento', 'change_medicamento', 'delete_medicamento',
                      'add_proveedor', 'change_proveedor', 'delete_proveedor']
    )
    grupo_administrador.permissions.set(permisos_administrador)

    # Asignar permisos a clientes
    permisos_cliente = Permission.objects.filter(
        codename__in=['view_venta', 'add_venta']
    )
    grupo_cliente.permissions.set(permisos_cliente)

class Medicamento(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(null=True, blank=True)  # Si es necesario
    stock = models.IntegerField(default=0)  # Si es necesario

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    stock = models.PositiveIntegerField()
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, default=1)
    cantidad_vendida = models.PositiveIntegerField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Venta de {self.medicamento.nombre}'

