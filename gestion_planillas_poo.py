# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Planillas y RRHH - Industrias Stark
Proyecto Final del Curso: Fundamentos de Programación 2
"""
import datetime


# --- CLASES MODELO (DATOS) ---

class Area:
    """Representa un área de la empresa (ej. TI, ADM)."""
    def __init__(self, nombre):
        self._nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    def __str__(self):
        return self._nombre


class Cargo:
    """Representa un cargo dentro de la empresa (ej. Junior, Senior)."""
    def __init__(self, nombre):
        self._nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    def __str__(self):
        return self._nombre


class Bono:
    """Representa un bono aplicable a un empleado."""
    def __init__(self, tipo, monto):
        self._tipo = tipo
        self.monto = monto

    def __str__(self):
        return f"{self._tipo}: S/.{self.monto:.2f}"


class DescuentoPrevisional:
    """Representa un descuento de ley (ej. AFP)."""
    def __init__(self, tipo, porcentaje):
        self._tipo = tipo
        self._porcentaje = porcentaje

    def aplicar(self, sueldo_bruto):
        return sueldo_bruto * (self._porcentaje / 100)


class BoletaDePago:
    """Representa la boleta de pago generada por un cálculo."""
    def __init__(self, sueldo_base, bonos, descuentos, neto):
        self._sueldo_base = sueldo_base
        self._total_bonos = bonos
        self._total_descuentos = descuentos
        self.sueldo_neto = neto

    def mostrar_detalle(self):
        print(f"\n   Salario Base:    S/.{self._sueldo_base:.2f}")
        print(f"   (+) Bonos:         S/.{self._total_bonos:.2f}")
        print(f"   (-) Descuentos:  S/.{self._total_descuentos:.2f}")
        print("   -------------------------")
        print(f"   SUELDO NETO:   S/.{self.sueldo_neto:.2f}")


class Evaluacion:
    """Gestiona la evaluación de desempeño de un empleado en un periodo."""
    def __init__(self, periodo, puntaje=0.0):
        self._periodo = periodo
        self._puntaje = puntaje
        self._avances = []
        self._asistencia_registrada = False

    @property
    def puntaje(self):
        return self._puntaje

    @property
    def estado_asistencia(self):
        return "Registrada" if self._asistencia_registrada else "Pendiente"

    def calificar(self, puntaje):
        self._puntaje = puntaje
        print(f"-> Calificación actualizada: {self._puntaje}/100 pts.")

    def agregar_avance(self, avance):
        self._avances.append(avance)
        print(f"-> Avance registrado: '{avance}'")

    def registrar_asistencia(self):
        self._asistencia_registrada = True


class Vacacion:
    """Representa una solicitud de vacaciones."""
    def __init__(self, fecha_inicio, fecha_fin):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = "Pendiente"

    def __str__(self):
        return (f"Del {self.fecha_inicio.strftime('%d/%m/%Y')} al "
                f"{self.fecha_fin.strftime('%d/%m/%Y')} (Estado: {self.estado})")


# --- CLASE PRINCIPAL DE NEGOCIO ---

class Empleado:
    """Representa a un empleado de la empresa y su lógica de negocio."""
    def __init__(self, dni, nombre, puesto, salario, area, cargo):
        self.dni = dni
        self.nombre = nombre
        self.puesto = puesto
        self.salario = salario
        self.area = area
        self.cargo = cargo
        self.bonos_aplicables = []
        self.vacaciones = []
        self.descuento_previsional = None
        self.evaluacion_actual = None
        self.bono_desempeno_base = None
        self._bono_por_avance_actual = None

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
                else:
                    print("Avance registrado. Aún no se alcanza un umbral para el bono.")
            return True
        return False

    def verificar_cumplimiento(self):
        if self.evaluacion_actual:
            puntaje = self.evaluacion_actual.puntaje
            meta_cumplida = puntaje >= 50
            estado_msg = "Aún no llega a una meta de bono."
            if puntaje >= 100:
                estado_msg = "Meta de bono completo CUMPLIDA."
            elif puntaje >= 50:
                estado_msg = "Meta de bono parcial CUMPLIDA."
            resultado_str = "Cumplido" if meta_cumplida else "No Cumplido"
            print(f"\n--- Verificación de Cumplimiento ---\n"
                  f"Empleado: {self.nombre}\n"
                  f"Puntaje: {puntaje}/100\n"
                  f"Estado: {estado_msg}\n"
                  f"Resultado: {resultado_str}\n"
                  f"-----------------------------------")
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
        if self._bono_por_avance_actual:
            bonos.append(self._bono_por_avance_actual)
        total_bonos = sum(b.monto for b in bonos)

        total_descuentos = 0
        if self.descuento_previsional:
            total_descuentos += self.descuento_previsional.aplicar(self.salario)
        total_descuentos += self.salario * 0.10  # Impuesto simulado

        sueldo_neto = self.salario + total_bonos - total_descuentos
        return BoletaDePago(self.salario, total_bonos, total_descuentos, sueldo_neto)

    def consultar_boleta_pago(self):
        print(f"\n--- Boleta de Pago para: {self.nombre} ---")
        boleta = self.calcular_boleta_pago()
        boleta.mostrar_detalle()

    def __str__(self):
        return f"DNI: {self.dni} | Nombre: {self.nombre} | Área: {self.area.nombre}"


# --- CLASES DE USUARIO (HERENCIA Y POLIMORFISMO) ---

class Usuario:
    """Clase base para todos los usuarios del sistema."""
    def __init__(self, nombre, contrasena):
        self._nombre = nombre
        self._contrasena = contrasena

    @property
    def nombre(self):
        return self._nombre

    def iniciar_sesion(self, contrasena):
        return self._contrasena == contrasena


class UsuarioEmpleado(Usuario):
    """Usuario con rol de Empleado."""
    def __init__(self, nombre, contrasena, empleado):
        super().__init__(nombre, contrasena)
        self.empleado = empleado


class UsuarioRRHH(Usuario):
    """Usuario con rol de Recursos Humanos."""
    def __init__(self, nombre, contrasena, controlador):
        super().__init__(nombre, contrasena)
        self._controlador = controlador

    def gestionar_empleados(self, *args):
        return self._controlador.registrar_empleado(*args)

    def verificar_estado(self, dni, tipo):
        empleado = self._controlador.buscar_empleado(dni)
        if not empleado:
            print("Error: No se encontró un empleado con ese DNI.")
            return
        if tipo == "asistencia":
            print(f"-> Estado de Asistencia: {empleado.estado_asistencia}")
        elif tipo == "cumplimiento":
            print(f"-> Puntaje de Cumplimiento: {empleado.estado_cumplimiento}")

    def revocar_bono_desempeno(self, dni):
        empleado = self._controlador.buscar_empleado(dni)
        if not empleado:
            print("Error: No se encontró un empleado con ese DNI.")
            return
        if empleado._bono_por_avance_actual:
            print(f"Bono por avance eliminado para el empleado {empleado.nombre}.")
            empleado._bono_por_avance_actual = None
        else:
            print(f"El empleado {empleado.nombre} no tiene un bono por avance activo para eliminar.")

    def gestionar_vacaciones(self, dni):
        empleado = self._controlador.buscar_empleado(dni)
        if not empleado:
            print("Error: No se encontró un empleado con ese DNI.")
            return

        pendientes = [v for v in empleado.vacaciones if v.estado == "Pendiente"]
        if not pendientes:
            print(f"El empleado no tiene solicitudes de vacaciones pendientes.")
            return

        print(f"\nSolicitudes pendientes para {empleado.nombre}:")
        for i, v in enumerate(pendientes, 1):
            print(f"  {i}. {v}")
        try:
            opcion = int(input("Elige el nro. de la solicitud a gestionar (0 para cancelar): "))
            if 0 < opcion <= len(pendientes):
                solicitud = pendientes[opcion - 1]
                accion = input("¿Desea 'aprobar' o 'rechazar' la solicitud? > ").lower()
                if accion == 'aprobar':
                    aprobadas = [v for v in empleado.vacaciones if v.estado == "Aprobada"]
                    hay_cruce = any(max(solicitud.fecha_inicio, v.fecha_inicio) <=
                                  min(solicitud.fecha_fin, v.fecha_fin) for v in aprobadas)
                    if hay_cruce:
                        print("Error: La solicitud se cruza con otras vacaciones ya aprobadas.")
                    else:
                        solicitud.estado = "Aprobada"
                        print("Solicitud aprobada.")
                elif accion == 'rechazar':
                    solicitud.estado = "Rechazada"
                    print("Solicitud rechazada.")
                else:
                    print("Acción no válida.")
        except ValueError:
            print("Debes ingresar un número válido.")


class UsuarioGerencia(Usuario):
    """Usuario con rol de Gerencia."""
    def __init__(self, nombre, contrasena, controlador):
        super().__init__(nombre, contrasena)
        self._controlador = controlador

    def generar_reporte(self, tipo):
        empleados = self._controlador.empleados
        if tipo == 1:
            print("\n--- REPORTE POR ÁREA ---")
            for e in empleados:
                print(f"- {e.nombre} | {e.area.nombre}")
        elif tipo == 2:
            print("\n--- REPORTE DE COSTO DE PLANILLA ---")
            costo = sum(e.calcular_boleta_pago().sueldo_neto for e in empleados)
            print(f"Costo Total de Sueldos Netos: S/.{costo:.2f}")


# --- PATRÓN CONTROLADOR Y FACTORY ---

class SistemaRRHH:
    """Clase controladora que centraliza la lógica y el estado del sistema."""
    def __init__(self):
        self._empleados = []
        self._usuarios_empleados = {}
        self._areas = {"TI": Area("Tecnología"), "ADM": Area("Administración")}
        self._cargos = {"JR": Cargo("Junior"), "SR": Cargo("Senior")}
        self._afp = DescuentoPrevisional("AFP", 12.0)
        self._bono_desemp = Bono("Desempeño Alto", 450.0)
        self._puestos_validos = [
            "Desarrollador Backend", "Desarrollador Frontend", "Analista QA", "DevOps",
            "Asistente Administrativo", "Contador", "Jefe de Operaciones", "Analista de Marketing"
        ]

    @property
    def empleados(self):
        return self._empleados

    @property
    def puestos_validos(self):
        return self._puestos_validos

    def buscar_empleado(self, dni):
        for emp in self._empleados:
            if emp.dni == dni:
                return emp
        return None

    def registrar_empleado(self, dni, nombre, puesto, salario, area_key, cargo_key):
        """Factory Method para crear y configurar un nuevo empleado y su usuario."""
        if self.buscar_empleado(dni):
            print("Error: DNI ya registrado.")
            return False

        area = self._areas.get(area_key.upper(), self._areas["TI"])
        cargo = self._cargos.get(cargo_key.upper(), self._cargos["JR"])

        empleado = Empleado(dni, nombre, puesto, salario, area, cargo)
        empleado.evaluacion_actual = Evaluacion(periodo="2025-Q4")
        empleado.descuento_previsional = self._afp
        empleado.bono_desempeno_base = self._bono_desemp

        # Lógica para crear un nombre de usuario único
        partes = nombre.strip().split()
        primer_nombre = partes[0].capitalize()
        inicial = partes[1][0].upper() if len(partes) > 1 else ""
        base_user = f"{primer_nombre}{inicial}"
        user = base_user
        i = 1
        while user in self._usuarios_empleados:
            user = f"{base_user}{i}"
            i += 1

        usuario = UsuarioEmpleado(user, "clave123", empleado)
        self._empleados.append(empleado)
        self._usuarios_empleados[usuario.nombre] = usuario
        print(f"Empleado {nombre} registrado.\n   Usuario: '{usuario.nombre}', Clave: 'clave123'.")
        return True


# --- MANEJADORES DE MENÚ (INTERFAZ DE USUARIO) ---

def manejar_menu_empleado(usuario):
    """Gestiona el bucle de menú para el rol de Empleado."""
    print("\n--- MENÚ EMPLEADO ---")
    print("1. Ver Boleta")
    print("2. Marcar Asistencia")
    print("3. Registrar Avance")
    print("4. Verificar Cumplimiento")
    print("5. Solicitar Vacaciones")
    print("6. Ver Estado de Vacaciones")
    print("7. Cerrar Sesión")
    opcion = input("Seleccione una opción > ")

    if opcion == '1':
        usuario.empleado.consultar_boleta_pago()
    elif opcion == '2':
        usuario.empleado.registrar_asistencia()
    elif opcion == '3':
        while True:
            try:
                porcentaje = float(input("Ingrese su porcentaje de avance (0-100) > "))
                if 0 <= porcentaje <= 100:
                    usuario.empleado.registrar_avance_trabajo(porcentaje)
                    break
                else:
                    print("Error: El porcentaje debe estar entre 0 y 100.")
            except ValueError:
                print("Error: Debe ingresar un valor numérico.")
    elif opcion == '4':
        usuario.empleado.verificar_cumplimiento()
    elif opcion == '5':
        try:
            inicio_str = input("Fecha de inicio (DD/MM/YYYY): ")
            fin_str = input("Fecha de fin (DD/MM/YYYY): ")
            fecha_inicio = datetime.datetime.strptime(inicio_str, "%d/%m/%Y").date()
            fecha_fin = datetime.datetime.strptime(fin_str, "%d/%m/%Y").date()
            if fecha_inicio > fecha_fin:
                print("Error: La fecha de inicio no puede ser posterior a la de fin.")
            elif (fecha_fin - fecha_inicio).days > 31:
                print("Error: No se pueden solicitar más de 31 días.")
            else:
                usuario.empleado.solicitar_vacaciones(fecha_inicio, fecha_fin)
        except ValueError:
            print("Error: Formato de fecha incorrecto. Usa DD/MM/YYYY.")
    elif opcion == '6':
        usuario.empleado.consultar_estado_vacaciones()
    elif opcion == '7':
        print("Sesión cerrada.")
        return None
    else:
        print("Opción no válida.")
    return usuario


def manejar_menu_rrhh(usuario, sistema):
    """Gestiona el bucle de menú para el rol de RRHH."""
    print("\n--- MENÚ RRHH ---")
    print("1. Registrar Empleado")
    print("2. Calcular Boleta")
    print("3. Ver Lista Empleados")
    print("4. Verificar Asistencia")
    print("5. Verificar Cumplimiento")
    print("6. Revocar Bono")
    print("7. Gestionar Vacaciones")
    print("8. Cerrar Sesión")
    opcion = input("Seleccione una opción > ")

    if opcion == '1':
        while True:
            dni = input("DNI (8 dígitos): ").strip()
            if dni.isdigit() and len(dni) == 8:
                break
            else:
                print("Error: El DNI debe contener exactamente 8 dígitos numéricos.")
        while True:
            nombre = input("Nombre completo: ").strip()
            partes = nombre.split()
            if nombre and len(partes) >= 2 and all(c.isalpha() or c.isspace() for c in nombre):
                break
            else:
                print("Error: Ingrese un nombre y apellido válidos (solo letras).")
        while True:
            print(f"Puestos disponibles: {', '.join(sistema.puestos_validos)}")
            puesto = input("Puesto: ").strip()
            if any(p.lower() == puesto.lower() for p in sistema.puestos_validos):
                puesto = [p for p in sistema.puestos_validos if p.lower() == puesto.lower()][0]
                break
            else:
                print(f"Error: Puesto no válido. Elija uno de la lista.")
        while True:
            try:
                salario = float(input("Salario (mínimo S/.1130): "))
                if salario >= 1130:
                    break
                else:
                    print("Error: El salario no puede ser menor al sueldo mínimo.")
            except ValueError:
                print("Error: Por favor, ingrese un monto numérico.")
        while True:
            area = input("Área (TI/ADM): ").strip().upper()
            if area in ["TI", "ADM"]:
                break
            else:
                print("Error: El área solo puede ser 'TI' o 'ADM'.")
        while True:
            cargo = input("Cargo (JR/SR): ").strip().upper()
            if cargo in ["JR", "SR"]:
                break
            else:
                print("Error: El cargo solo puede ser 'JR' o 'SR'.")
        usuario.gestionar_empleados(dni, nombre, puesto, salario, area, cargo)
    elif opcion in ['2', '4', '5', '6', '7']:
        dni = input("Ingrese el DNI del empleado > ")
        empleado = sistema.buscar_empleado(dni)
        if not empleado:
            print("Error: No se encontró un empleado con ese DNI.")
            return usuario
        if opcion == '2':
            empleado.consultar_boleta_pago()
        elif opcion == '4':
            usuario.verificar_estado(dni, "asistencia")
        elif opcion == '5':
            usuario.verificar_estado(dni, "cumplimiento")
        elif opcion == '6':
            usuario.revocar_bono_desempeno(dni)
        elif opcion == '7':
            usuario.gestionar_vacaciones(dni)
    elif opcion == '3':
        print("\n--- LISTA DE EMPLEADOS ---")
        if not sistema.empleados:
            print("No hay empleados registrados.")
        for emp in sistema.empleados:
            print(emp)
    elif opcion == '8':
        print("Sesión cerrada.")
        return None
    else:
        print("Opción no válida.")
    return usuario


def manejar_menu_gerencia(usuario, sistema):
    """Gestiona el bucle de menú para el rol de Gerencia."""
    print("\n--- MENÚ GERENCIA ---")
    print("1. Reporte por Área")
    print("2. Reporte de Costo de Planilla")
    print("3. Cerrar Sesión")
    opcion = input("Jarvis: ¿Qué necesita, señor? > ")

    if opcion == '1':
        usuario.generar_reporte(1)
    elif opcion == '2':
        usuario.generar_reporte(2)
    elif opcion == '3':
        print("Jarvis: Desconectando. Que tenga un buen día, señor Stark.")
        return None
    else:
        print("Jarvis: Señor, esa no es una opción válida en mis protocolos.")
    return usuario


# --- FUNCIÓN PRINCIPAL (PUNTO DE ENTRADA) ---

def main():
    """Función principal que inicia y controla el flujo del programa."""
    sistema = SistemaRRHH()
    usuarios_sistema = {
        "RRHH": UsuarioRRHH("RRHH", "123", sistema),
        "tonystark": UsuarioGerencia("tonystark", "9000", sistema)
    }
    
    sistema.registrar_empleado("74889304", "Renato Prado", "Desarrollador Backend", 3500.0, "TI", "JR")
    
    print("--- SISTEMA DE GESTIÓN DE PLANILLAS STARK ---")
    usuario_actual = None
    while True:
        try:
            if usuario_actual is None:
                print("\n--- INICIO DE SESIÓN ---")
                nombre = input("Usuario (o escriba 'salir' para terminar): ").strip()
                if nombre.lower() == 'salir':
                    print("Gracias por usar el Sistema de Planillas Stark. ¡Hasta luego!")
                    break
                
                contrasena = input("Contraseña: ").strip()
                usuario = usuarios_sistema.get(nombre) or sistema._usuarios_empleados.get(nombre)
                
                if usuario and usuario.iniciar_sesion(contrasena):
                    usuario_actual = usuario
                    if usuario_actual.nombre == "tonystark":
                        print("\nJarvis: Bienvenido de vuelta, señor.")
                    else:
                        print(f"\nBienvenido, {usuario_actual.nombre}.")
                else:
                    print("Usuario o contraseña incorrectos.")
                continue
            
            # Flujo principal basado en polimorfismo
            if isinstance(usuario_actual, UsuarioEmpleado):
                usuario_actual = manejar_menu_empleado(usuario_actual)
            elif isinstance(usuario_actual, UsuarioRRHH):
                usuario_actual = manejar_menu_rrhh(usuario_actual, sistema)
            elif isinstance(usuario_actual, UsuarioGerencia):
                usuario_actual = manejar_menu_gerencia(usuario_actual, sistema)
        
        except ValueError:
            print("\nError: Se esperaba un valor numérico donde se ingresó texto.")
        except Exception as e:
            print(f"\nHa ocurrido un error inesperado: {e}")


if __name__ == "__main__":
    main()