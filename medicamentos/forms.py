from django import forms
from .models import Medicamento, Proveedor

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'precio', 'descripcion', 'stock']  # Asegúrate de que estos campos existan

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'direccion', 'producto']  # Los campos que deseas editar

