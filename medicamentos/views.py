from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Medicamento, Proveedor, Venta
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Sum
from .forms import MedicamentoForm, ProveedorForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def mi_funcion(request):
    # Aquí importamos el modelo solo cuando lo necesitemos
    from medicamentos.models import Medicamento

    # Ahora podemos realizar la consulta de base de datos
    medicamentos = Medicamento.objects.all()

    return render(request, 'mi_template.html', {'medicamentos': medicamentos})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_home')  # Redirige al panel admin si el usuario es superusuario
        else:
            error_message = "Credenciales incorrectas o no tiene permisos de superusuario."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

# Vista para el área de admin
@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    return render(request, 'admin.html')

# Vista para mostrar los medicamentos disponibles
def comprar_medicamentos(request):
    # Obtener todos los medicamentos de la base de datos
    medicamentos = Medicamento.objects.all()
    
    # Pasar los medicamentos al contexto
    return render(request, 'comprar_medicamentos.html', {'medicamentos': medicamentos})
# Vista para ver los medicamentos y agregar al carrito
@login_required
def ver_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'comprar_medicamentos.html', {'medicamentos': medicamentos})

# Vista para agregar productos al carrito

def finalizar_compra(request):
    # Aquí puedes agregar la lógica para finalizar la compra
    return render(request, 'finalizar_compra.html')

# Vista para realizar el pago
def realizar_pago(request):
    if request.method == 'POST':
        # Suponiendo que los datos de la compra están en el POST
        producto = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        precio = float(request.POST.get('precio'))
        cliente = request.POST.get('cliente')  # Puedes obtener el cliente de la sesión o de un formulario

        # Calcular el total
        total = cantidad * precio

        # Guardar la venta en la base de datos
        venta = Venta.objects.create(
            producto=producto,
            cantidad=cantidad,
            precio=precio,
            total=total,
            cliente=cliente
        )

        # Redirigir al historial de ventas o a otra página
        return redirect('historial_ventas')

    return render(request, 'realizar_pago.html')  # Página donde el cliente realiza el pago

def lista_medicamentos(request):
    # Obtener todos los medicamentos, asegurándose de que tienen un id válido
    medicamentos = Medicamento.objects.all()
    return render(request, 'lista_medicamentos.html', {'medicamentos': medicamentos})

def nuevo_medicamento(request):
    if request.method == 'POST':
        # Recuperar los datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        stock = request.POST.get('stock')
        precio = request.POST.get('precio')

        # Crear el nuevo medicamento
        Medicamento.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            stock=int(stock),
            precio=float(precio)
        )

        return redirect('admin_home')  # Cambia por la URL a la que deseas redirigir

    return render(request, 'nuevo_medicamento.html')

def modificar_medicamento(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        medicamento = Medicamento.objects.filter(nombre=nombre).first()

        if not medicamento:
            medicamento = Medicamento(nombre=nombre)

        medicamento.descripcion = request.POST['descripcion']
        medicamento.stock = int(request.POST['stock'])
        medicamento.precio = float(request.POST['precio'])
        medicamento.save()
        return redirect('admin_home')

    return render(request, 'modificar_medicamento.html', {'medicamento': None})

def eliminar_medicamento(request, medicamento_slug):
    medicamento = get_object_or_404(Medicamento, slug=medicamento_slug)

    if request.method == 'POST':
        medicamento.delete()
        return redirect('lista_medicamentos')  # Asegúrate de tener la URL correcta para la lista de medicamentos

    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})

def eliminar_proveedor(request, nombre):
    proveedor = get_object_or_404(Proveedor, nombre=nombre)
    proveedor.delete()
    return redirect('proveedores')  # O la URL que corresponda

def custom_logout(request):
    logout(request)
    return redirect('admin_home')

def lista_proveedores(request):
    proveedores = Proveedor.objects.all()  # Asegúrate de tener un modelo llamado Proveedor
    return render(request, 'proveedores.html', {'proveedores': proveedores})

def proveedores_list(request):
    proveedores = Proveedor.objects.all()  # Obtiene todos los proveedores
    return render(request, 'proveedores_list.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contacto = request.POST.get('contacto')
        direccion = request.POST.get('direccion')
        producto = request.POST.get('producto')

        # Crear nuevo proveedor
        proveedor = Proveedor(nombre=nombre, contacto=contacto, direccion=direccion, producto=producto)
        proveedor.save()

        return redirect('proveedores_list')  # Asegúrate de que esta URL sea válida
    return render(request, 'nuevo_proveedor.html')

def editar_proveedor(request, proveedor_nombre):
    proveedor = get_object_or_404(Proveedor, nombre=proveedor_nombre)  # Busca el proveedor por nombre
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')  # Redirige a la lista de proveedores después de guardar
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form, 'proveedor': proveedor})

def eliminar_proveedor(request, proveedor_nombre):
    # Buscar el proveedor por nombre
    proveedor = get_object_or_404(Proveedor, nombre=proveedor_nombre)

    if request.method == 'POST':
        proveedor.delete()  # Elimina el proveedor
        return redirect('proveedores_list')  # Redirige a la lista de proveedores

    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})

def ventas(request):
    return render(request, 'ventas.html')

def historial_ventas(request):
    # Obtener todas las ventas realizadas
    ventas = Venta.objects.all()

    return render(request, 'ventas.html', {'ventas': ventas})

def registrar_venta(request):
    # Obtener todos los medicamentos disponibles
    medicamentos = Medicamento.objects.all()

    # Para calcular el total de dinero ganado en las ventas
    total_dinero = Venta.objects.aggregate(Sum('total_venta'))['total_venta__sum'] or 0

    # Obtener las ventas registradas
    ventas = Venta.objects.all()

    if request.method == 'POST':
        # Obtener los datos del formulario
        medicamento_id = request.POST.get('medicamento')
        cantidad_vendida = int(request.POST.get('cantidad_vendida'))

        # Buscar el medicamento seleccionado por el usuario
        medicamento = Medicamento.objects.get(id=medicamento_id)

        # Calcular el total de la venta (precio del medicamento * cantidad)
        total_venta = medicamento.precio * cantidad_vendida

        # Crear una nueva venta y guardarla
        nueva_venta = Venta(medicamento=medicamento, cantidad_vendida=cantidad_vendida, total_venta=total_venta)
        nueva_venta.save()

        # Redirigir a la vista de ventas (puedes poner la URL que corresponda)
        return redirect('ventas')  # Asegúrate de que 'ventas' esté definido en tus URLs

    # Pasar los medicamentos y ventas al contexto para renderizar la plantilla
    context = {
        'medicamentos': medicamentos,
        'ventas': ventas,
        'total_dinero': total_dinero,
    }

    # Renderizar el template con el contexto
    return render(request, 'registrar_venta.html', context)

def registrar_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_medicamentos')
    else:
        form = MedicamentoForm()
    return render(request, 'registrar_medicamento.html', {'form': form})

