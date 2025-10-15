"""
Sistema de Gestión de Planillas y RRHH - Industrias Stark
Proyecto Final del Curso: Fundamentos de Programación 2
"""
import datetime

# --- CLASES MODELO (DATOS) ---
class Area:
    """Representa un área de la empresa (ej. TI, ADM)."""
    def _init_(self, nombre): self._nombre = nombre
    @property
    def nombre(self): return self._nombre
    def _str_(self): return self._nombre


class Cargo:
    """Representa un cargo dentro de la empresa (ej. Junior, Senior)."""
    def _init_(self, nombre): self._nombre = nombre
    @property
    def nombre(self): return self._nombre
    def _str_(self): return self._nombre


class Bono:
    """Representa un bono aplicable a un empleado."""
    def _init_(self, tipo, monto): self._tipo, self.monto = tipo, monto
    def _str_(self): return f"{self._tipo}: S/.{self.monto:.2f}"


class DescuentoPrevisional:
    """Representa un descuento de ley (ej. AFP)."""
    def _init_(self, tipo, porcentaje): self._tipo, self._porcentaje = tipo, porcentaje
    def aplicar(self, sueldo_bruto): return sueldo_bruto * (self._porcentaje / 100)


class BoletaDePago:
    """Representa la boleta de pago generada por un cálculo."""
    def _init_(self, sueldo_base, bonos, descuentos, neto):
        self._sueldo_base, self._total_bonos = sueldo_base, bonos
        self._total_descuentos, self.sueldo_neto = descuentos, neto
    def mostrar_detalle(self):
        print(f"\n   Salario Base:    S/.{self._sueldo_base:.2f}")
        print(f"   (+) Bonos:         S/.{self._total_bonos:.2f}")
        print(f"   (-) Descuentos:  S/.{self._total_descuentos:.2f}")
        print("   -------------------------")
        print(f"   SUELDO NETO:   S/.{self.sueldo_neto:.2f}")
