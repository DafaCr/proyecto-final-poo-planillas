# test_sistema_rrhh.py

import unittest
# Se importa la clase Evaluacion también
from gestion_planillas_poo import Empleado, Area, Cargo, Bono, DescuentoPrevisional, SistemaRRHH, Evaluacion

class TestCalculosEmpleado(unittest.TestCase):
    """
    Esta clase agrupa todas las pruebas relacionadas con los cálculos de la clase Empleado.
    """

    def setUp(self):
        """
        Este método especial se ejecuta ANTES de cada prueba.
        """
        self.area_test = Area("Pruebas")
        self.cargo_test = Cargo("Tester")
        self.bono_base_test = Bono("Desempeño Alto", 450.0)

    def test_calculo_boleta_simple(self):
        """Prueba el cálculo de sueldo neto solo con el impuesto de ley."""
        # 1. Arrange (Preparar)
        empleado = Empleado("11111111", "Juan Test", "Tester", 1000.0, self.area_test, self.cargo_test)
        
        # 2. Act (Actuar)
        boleta = empleado.calcular_boleta_pago()
        
        # 3. Assert (Verificar)
        self.assertEqual(boleta.sueldo_neto, 900.0)

    def test_calculo_boleta_con_afp(self):
        """Prueba el cálculo de sueldo neto incluyendo el descuento de AFP."""
        # 1. Arrange (Preparar)
        empleado = Empleado("22222222", "Maria Test", "Tester", 2000.0, self.area_test, self.cargo_test)
        empleado.descuento_previsional = DescuentoPrevisional("AFP", 10.0)
        
        # 2. Act (Actuar)
        boleta = empleado.calcular_boleta_pago()
        
        # 3. Assert (Verificar)
        self.assertEqual(boleta.sueldo_neto, 1600.0)

    def test_calculo_con_bono_automatico_completo(self):
        """Prueba que el bono por avance al 100% se sume correctamente."""
        # Esta prueba funcionaba porque usaba registrar_empleado, que sí crea una Evaluación.
        # 1. Arrange (Preparar)
        sistema = SistemaRRHH() 
        sistema.registrar_empleado("33333333", "Carlos Test", "Dev", 3000.0, "TI", "JR")
        empleado = sistema.buscar_empleado("33333333")
        
        empleado.registrar_avance_trabajo(100)
        
        # 2. Act (Actuar)
        boleta = empleado.calcular_boleta_pago()
        
        # 3. Assert (Verificar)
        self.assertAlmostEqual(boleta.sueldo_neto, 2790.0)

    def test_calculo_con_bono_automatico_parcial(self):
        """Prueba que el bono por avance al 50% se sume correctamente."""
        # 1. Arrange (Preparar)
        empleado = Empleado("44444444", "Lucia Test", "Diseñadora", 4000.0, self.area_test, self.cargo_test)
        empleado.bono_desempeno_base = self.bono_base_test
        
        # ▼▼▼ LÍNEA CORREGIDA/AÑADIDA ▼▼▼
        # Se le asigna un objeto Evaluacion para que el método de avance funcione.
        empleado.evaluacion_actual = Evaluacion("periodo-test")
        
        empleado.registrar_avance_trabajo(50)
        
        # 2. Act (Actuar)
        boleta = empleado.calcular_boleta_pago()
        
        # 3. Assert (Verificar)
        # Salario (4000) + Medio Bono (225) - Impuesto (10% de 4000 = 400) = 3825
        self.assertAlmostEqual(boleta.sueldo_neto, 3825.0)

if __name__ == '__main__':
    unittest.main()