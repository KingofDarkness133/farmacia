from django.apps import AppConfig
from .models import Medicamento, Venta  # Esto puede causar conflictos

class MedicamentosConfig(AppConfig):
    name = 'medicamentos'

    def ready(self):
        from .models import Medicamento, Venta  # Duplicado