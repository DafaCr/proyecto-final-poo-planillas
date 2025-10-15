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
        
class Evaluacion:
    """Gestiona la evaluación de desempeño de un empleado en un periodo."""
    def __init__(self, periodo, puntaje=0.0):
        self._periodo, self._puntaje = periodo, puntaje
        self._avances, self._asistencia_registrada = [], False
    @property
    def puntaje(self): return self._puntaje
    @property
    def estado_asistencia(self): return "Registrada" if self._asistencia_registrada else "Pendiente"
    def calificar(self, puntaje): self._puntaje = puntaje; print(f"-> Calificación actualizada: {self._puntaje}/100 pts.")
    def agregar_avance(self, avance): self._avances.append(avance); print(f"-> Avance registrado: '{avance}'")
    def registrar_asistencia(self): self._asistencia_registrada = True


class Vacacion:
    """Representa una solicitud de vacaciones."""
    def __init__(self, fecha_inicio, fecha_fin):
        self.fecha_inicio, self.fecha_fin, self.estado = fecha_inicio, fecha_fin, "Pendiente"
    def __str__(self):
        return (f"Del {self.fecha_inicio.strftime('%d/%m/%Y')} al "
                f"{self.fecha_fin.strftime('%d/%m/%Y')} (Estado: {self.estado})")


class Empleado:
    """Representa a un empleado de la empresa y su lógica de negocio."""
    def __init__(self, dni, nombre, puesto, salario, area, cargo):
        self.dni, self.nombre, self.puesto, self.salario = dni, nombre, puesto, salario
        self.area, self.cargo = area, cargo
        self.bonos_aplicables, self.vacaciones = [], []
        self.descuento_previsional, self.evaluacion_actual = None, None
        self.bono_desempeno_base, self._bono_por_avance_actual = None, None
    
    @property
    def estado_cumplimiento(self):
        return f"{self.evaluacion_actual.puntaje}/100" if self.evaluacion_actual else "No Evaluado"
    @property
    def estado_asistencia(self):
        return self.evaluacion_actual.estado_asistencia if self.evaluacion_actual else "No Verificable"

    def registrar_asistencia(self):
        if self.evaluacion_actual:
            self.evaluacion_actual.registrar_asistencia()
            print(f"Asistencia de {self.nombre} marcada correctamente para hoy.")
    
    def registrar_avance_trabajo(self, porcentaje):
        if self.evaluacion_actual:
            self.evaluacion_actual.agregar_avance(f"Avance del {porcentaje}% en la tarea.")
            self.evaluacion_actual.calificar(porcentaje)
            self._bono_por_avance_actual = None
            if self.bono_desempeno_base:
                if porcentaje >= 100:
                    monto = self.bono_desempeno_base.monto
                    print(f"Se ha generado el bono completo de S/.{monto:.2f} por cumplimiento.")
                    self._bono_por_avance_actual = Bono("Bono por Cumplimiento Total", monto)
                elif porcentaje >= 50:
                    monto = self.bono_desempeno_base.monto / 2
                    print(f"Se ha generado medio bono de S/.{monto:.2f} por cumplimiento parcial.")
                    self._bono_por_avance_actual = Bono("Bono por Cumplimiento Parcial", monto)
                else: print("Avance registrado. Aún no se alcanza un umbral para el bono.")
            return True
        return False
        
    def verificar_cumplimiento(self):
        if self.evaluacion_actual:
            puntaje = self.evaluacion_actual.puntaje; meta_cumplida = puntaje >= 50
            estado_msg = "Aún no llega a una meta de bono."
            if puntaje >= 100: estado_msg = "Meta de bono completo CUMPLIDA."
            elif puntaje >= 50: estado_msg = "Meta de bono parcial CUMPLIDA."
            resultado_str = "Cumplido" if meta_cumplida else "No Cumplido"
            print(f"\n--- Verificación de Cumplimiento ---\nEmpleado: {self.nombre}\nPuntaje: {puntaje}/100\nEstado: {estado_msg}\nResultado: {resultado_str}\n-----------------------------------")
            return meta_cumplida
        return False
    
    def solicitar_vacaciones(self, fecha_inicio, fecha_fin):
        self.vacaciones.append(Vacacion(fecha_inicio, fecha_fin))
        print("Solicitud de vacaciones registrada. RRHH la revisará pronto.")
    
    def consultar_estado_vacaciones(self):
        print(f"\n--- Estado de Solicitudes de Vacaciones: {self.nombre} ---")
        if not self.vacaciones:
            print("No tienes ninguna solicitud de vacaciones registrada.")
            return
        for i, vacacion in enumerate(self.vacaciones, 1):
            print(f"{i}. {vacacion}")

    def calcular_boleta_pago(self):
        bonos = self.bonos_aplicables[:]
        if self._bono_por_avance_actual: bonos.append(self._bono_por_avance_actual)
        total_bonos = sum(b.monto for b in bonos)
        
        total_descuentos = 0
        if self.descuento_previsional: total_descuentos += self.descuento_previsional.aplicar(self.salario)
        total_descuentos += self.salario * 0.10
        
        sueldo_neto = self.salario + total_bonos - total_descuentos
        return BoletaDePago(self.salario, total_bonos, total_descuentos, sueldo_neto)

    def consultar_boleta_pago(self):
        print(f"\n--- Boleta de Pago para: {self.nombre} ---")
        self.calcular_boleta_pago().mostrar_detalle()

    def __str__(self): return f"DNI: {self.dni} | Nombre: {self.nombre} | Área: {self.area.nombre}"