from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL para el login
    path('admin-home/', views.admin_home, name='admin_home'),  # URL para el área de administración
    path('', views.index, name='index'),  # Página principal (opcional)
    path('medicamentos/', views.ver_medicamentos, name='ver_medicamentos'),
    
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),  # Finalizar compra
    # URL para realizar el pago
    path('realizar_pago/', views.realizar_pago, name='realizar_pago'),
    # URL para la página de compra de medicamentos
    path('comprar/', views.comprar_medicamentos, name='comprar_medicamentos'),
    
    path('admin-home/', views.lista_medicamentos, name='admin_home'),
    path('medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('admin-lista_medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path('modificar_medicamento/', views.modificar_medicamento, name='modificar_medicamento'),
    path('nuevo_medicamento/', views.nuevo_medicamento, name='nuevo_medicamento'),
    path('eliminar-medicamento/<slug:medicamento_slug>/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('lista-medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('proveedores/', views.lista_proveedores, name='proveedores'),
    path('agregar_proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/', views.proveedores_list, name='proveedores_list'),  # Asegúrate de que esta línea esté presente
    path('proveedor/<str:proveedor_nombre>/editar/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar-proveedor/<str:nombre>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('ventas/', views.ventas, name='ventas'),
    path('realizar_pago/', views.realizar_pago, name='realizar_pago'),
    path('historial_ventas/', views.historial_ventas, name='historial_ventas'),
    path('registrar-venta/', views.registrar_venta, name='registrar_venta'),
]