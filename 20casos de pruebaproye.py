"""
Casos de Prueba para el Simulador de Red LAN Inteligente
Proyecto Final - Redes Computacionales y Análisis de Algoritmos
"""

import unittest
import time
import sys
import os

# Importar las clases del simulador
from proyecto import LanSimulator, LanNode, Emergency

class TestLanSimulator(unittest.TestCase):
    """Clase de pruebas unitarias para el simulador LAN"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.simulator = LanSimulator()
        self.setup_basic_topology()
    
    def setup_basic_topology(self):
        """Configura una topología básica para las pruebas"""
        # Crear nodos
        central = LanNode("N1", "Estación Central", "CENTRAL", (50, 50))
        central.add_resource("AMBULANCIA", 5)
        central.add_resource("BOMBEROS", 3)
        central.add_resource("POLICIA", 4)
        
        norte = LanNode("N2", "Estación Norte", "ESTACION", (20, 80))
        norte.add_resource("AMBULANCIA", 2)
        norte.add_resource("POLICIA", 3)
        
        sur = LanNode("N3", "Estación Sur", "ESTACION", (80, 20))
        sur.add_resource("BOMBEROS", 3)
        sur.add_resource("PROTECCION_CIVIL", 2)
        
        router_este = LanNode("N4", "Router Este", "ROUTER", (90, 50))
        router_oeste = LanNode("N5", "Router Oeste", "ROUTER", (10, 50))
        
        # Agregar nodos al simulador
        for node in [central, norte, sur, router_este, router_oeste]:
            self.simulator.add_node(node)
        
        # Crear conexiones
        connections = [
            ("N1", "N2", 5.0),
            ("N1", "N3", 4.5),
            ("N1", "N4", 3.0),
            ("N1", "N5", 3.5),
            ("N2", "N5", 2.0),
            ("N3", "N4", 2.5)
        ]
        
        for node1, node2, weight in connections:
            self.simulator.add_connection(node1, node2, weight)
            
        # Validar que todos los nodos se agregaron
        self.assertEqual(len(self.simulator.nodes), 5)
        
        # Validar conexiones
        self.assertGreater(len(self.simulator.connections), 0)

class TestCase1_IncendioZonaResidencial(TestLanSimulator):
   # """Caso de Prueba 1: Incendio en zona residencial"""
    
    def test_incendio_zona_norte(self):
        #"""Prueba respuesta a incendio en zona residencial norte"""
        print("\n=== CASO 1: INCENDIO EN ZONA RESIDENCIAL ===")
        
        # Crear emergencia de incendio
        emergency = Emergency("E1", "INCENDIO", (25, 85))
        self.simulator.add_emergency(emergency)
        
        print(f"Emergencia creada: {emergency}")
        print(f"Ubicación: {emergency.location}")
        print(f"Prioridad: {emergency.priority}")
        print(f"Recursos requeridos: {emergency.required_resources}")
        
        # Procesar emergencia
        processed_emergency, assigned_node, path = self.simulator.process_next_emergency()
        
        # Verificaciones
        self.assertIsNotNone(processed_emergency)
        self.assertIsNotNone(assigned_node)
        self.assertEqual(processed_emergency.emergency_id, "E1")
        self.assertEqual(processed_emergency.emergency_type, "INCENDIO")
        self.assertEqual(processed_emergency.status, "COMPLETADA")
        
        # El nodo asignado debe tener bomberos
        self.assertTrue(assigned_node.has_resource("BOMBEROS"))
        
        print(f"✓ Emergencia asignada a: {assigned_node.name}")
        print(f"✓ Tiempo de respuesta: {processed_emergency.get_response_time():.2f}s")
        print(f"✓ Estado: {processed_emergency.status}")

class TestCase2_AccidenteTrafico(TestLanSimulator):
    #"""Caso de Prueba 2: Accidente de tráfico múltiple"""
    
    def test_accidente_multiples_recursos(self):
        #"""Prueba respuesta a accidente que requiere múltiples recursos"""
        print("\n=== CASO 2: ACCIDENTE DE TRÁFICO MÚLTIPLE ===")
        
        # Crear emergencia de accidente
        emergency = Emergency("E2", "ACCIDENTE_TRAFICO", (75, 25))
        self.simulator.add_emergency(emergency)
        
        print(f"Emergencia creada: {emergency}")
        print(f"Recursos requeridos: {emergency.required_resources}")
        
        # Procesar emergencia
        processed_emergency, assigned_node, path = self.simulator.process_next_emergency()
        
        # Verificaciones
        self.assertIsNotNone(processed_emergency)
        self.assertIsNotNone(assigned_node)
        
        # El nodo debe tener ambulancia Y policía
        self.assertTrue(assigned_node.has_resource("AMBULANCIA"))
        self.assertTrue(assigned_node.has_resource("POLICIA"))
        
        print(f"✓ Emergencia asignada a: {assigned_node.name}")
        print(f"✓ Nodo tiene ambulancia: {assigned_node.has_resource('AMBULANCIA')}")
        print(f"✓ Nodo tiene policía: {assigned_node.has_resource('POLICIA')}")

class TestCase3_FallaNodo(TestLanSimulator):
    #"""Caso de Prueba 3: Simulación de falla de nodo"""
    
    def test_falla_nodo_central(self):
        #"""Prueba el comportamiento cuando falla el nodo central"""
        print("\n=== CASO 3: FALLA DE NODO CENTRAL ===")
        
        # Verificar estado inicial
        central_node = self.simulator.nodes["N1"]
        self.assertTrue(central_node.active)
        
        # Simular falla del nodo central
        self.simulator.simulate_node_failure("N1")
        self.assertFalse(central_node.active)
        print("✓ Nodo central N1 desactivado")
        
        # Crear emergencia médica
        emergency = Emergency("E3", "EMERGENCIA_MEDICA", (60, 60))
        self.simulator.add_emergency(emergency)
        
        # Procesar emergencia (no debería usar N1)
        processed_emergency, assigned_node, path = self.simulator.process_next_emergency()
        
        if assigned_node:
            self.assertNotEqual(assigned_node.node_id, "N1")
            self.assertTrue(assigned_node.active)
            print(f"✓ Emergencia redirigida a: {assigned_node.name}")
        else:
            print("⚠ No se pudo procesar la emergencia (falta de recursos)")
        
        # Restaurar nodo
        self.simulator.restore_node("N1")
        self.assertTrue(central_node.active)
        print("✓ Nodo central restaurado")

class TestCase4_ColaPrioridades(TestLanSimulator):
    #"""Caso de Prueba 4: Cola de prioridades con múltiples emergencias"""
    
    def test_orden_prioridades(self):
        #"""Prueba el orden correcto de procesamiento por prioridades"""
        print("\n=== CASO 4: COLA DE PRIORIDADES ===")
        
        # Crear emergencias con diferentes prioridades y timestamps
        emergencies_data = [
            ("E1", "VANDALISMO", (30, 30), time.time()),      # Prioridad BAJA (1)
            ("E2", "INCENDIO", (40, 40), time.time() + 5),    # Prioridad ALTA (3)
            ("E3", "ROBO", (35, 35), time.time() + 3),        # Prioridad MEDIA (2)
            ("E4", "EMERGENCIA_MEDICA", (45, 45), time.time() + 7)  # Prioridad ALTA (3)
        ]
        
        # Agregar emergencias en orden de llegada
        for e_id, e_type, location, timestamp in emergencies_data:
            emergency = Emergency(e_id, e_type, location, timestamp)
            self.simulator.add_emergency(emergency)
            print(f"Agregada: {e_id} - {e_type} (Prioridad: {emergency.priority})")
        
        # Procesar emergencias y verificar orden
        expected_order = ["E2", "E4", "E3", "E1"]  # Por prioridad y timestamp
        processed_order = []
        
        while self.simulator.emergencies:
            emergency, node, path = self.simulator.process_next_emergency()
            if emergency:
                processed_order.append(emergency.emergency_id)
                print(f"Procesada: {emergency.emergency_id} - {emergency.emergency_type}")
        
        print(f"Orden esperado: {expected_order}")
        print(f"Orden procesado: {processed_order}")
        
        # Verificar que las emergencias de alta prioridad se procesaron primero
        high_priority_processed = processed_order[:2]
        self.assertIn("E2", high_priority_processed)  # Incendio
        self.assertIn("E4", high_priority_processed)  # Emergencia médica

class TestCase5_BusquedaZonas(TestLanSimulator):
   # """Caso de Prueba 5: Búsqueda geográfica por zonas"""
    
    def test_busqueda_por_zonas(self):
        #"""Prueba la funcionalidad de búsqueda por zonas geográficas"""
        print("\n=== CASO 5: BÚSQUEDA POR ZONAS ===")
        
        # Crear emergencias en diferentes zonas
        zone_emergencies = [
            Emergency("Z1", "INCENDIO", (15, 15)),      # Zona 1_1
            Emergency("Z2", "ROBO", (25, 15)),          # Zona 2_1
            Emergency("Z3", "VANDALISMO", (15, 25)),    # Zona 1_2
            Emergency("Z4", "INCENDIO", (18, 17))       # Zona 1_1 (misma que Z1)
        ]
        
        for emergency in zone_emergencies:
            self.simulator.add_emergency(emergency)
            zone_key = self.simulator._get_zone_key(emergency.location)
            print(f"Emergencia {emergency.emergency_id} en zona {zone_key}")
        
        # Buscar emergencias en zona específica
        zone_1_1_emergencies = self.simulator.get_emergencies_in_zone((15, 15))
        
        print(f"Emergencias en zona (15,15): {len(zone_1_1_emergencies)}")
        for emergency in zone_1_1_emergencies:
            print(f"  - {emergency.emergency_id}: {emergency.emergency_type}")
        
        # Verificar que hay exactamente 2 emergencias en la zona 1_1
        self.assertEqual(len(zone_1_1_emergencies), 2)
        emergency_ids = [e.emergency_id for e in zone_1_1_emergencies]
        self.assertIn("Z1", emergency_ids)
        self.assertIn("Z4", emergency_ids)

class TestCase6_RendimientoAltaCarga(TestLanSimulator):
    #"""Caso de Prueba 6: Análisis de rendimiento con carga alta"""
    
    def test_rendimiento_alta_carga(self):
        #Prueba el rendimiento del sistema con alta carga de emergencias"""
        print("\n=== CASO 6: RENDIMIENTO CON ALTA CARGA ===")
        
        # Generar topología más grande
        large_simulator = LanSimulator()
        large_simulator.generate_random_topology(num_nodes=20, connection_density=0.4)
        
        print(f"Topología generada: {len(large_simulator.nodes)} nodos")
        
        # Generar múltiples emergencias
        num_emergencies = 50
        start_time = time.time()
        
        for i in range(num_emergencies):
            emergency = large_simulator.generate_random_emergency()
        
        generation_time = time.time() - start_time
        print(f"Tiempo de generación de {num_emergencies} emergencias: {generation_time:.3f}s")
        
        # Procesar emergencias
        start_time = time.time()
        processed_count = 0
        
        while large_simulator.emergencies and processed_count < num_emergencies:
            emergency, node, path = large_simulator.process_next_emergency()
            if emergency:
                processed_count += 1
        
        processing_time = time.time() - start_time
        print(f"Tiempo de procesamiento: {processing_time:.3f}s")
        print(f"Emergencias procesadas: {processed_count}/{num_emergencies}")
        
        # Calcular métricas de rendimiento
        avg_time_per_emergency = processing_time / max(processed_count, 1)
        success_rate = (processed_count / num_emergencies) * 100
        
        print(f"Tiempo promedio por emergencia: {avg_time_per_emergency:.4f}s")
        print(f"Tasa de éxito: {success_rate:.1f}%")
        
        # Verificar que el rendimiento es aceptable
        self.assertLess(avg_time_per_emergency, 0.1)  # Menos de 0.1s por emergencia
        self.assertGreater(success_rate, 80)  # Al menos 80% de éxito

class TestCase7_RecuperacionFallos(TestLanSimulator):
            #Caso de Prueba 7: Recuperación de fallos múltiples
    
    def test_recuperacion_fallos_multiples(self):
       # """Prueba la recuperación del sistema ante múltiples fallos"""
        print("\n=== CASO 7: RECUPERACIÓN DE FALLOS MÚLTIPLES ===")
        
        # Estado inicial
        initial_active = sum(1 for node in self.simulator.nodes.values() if node.active)
        print(f"Nodos activos inicialmente: {initial_active}")
        
        # Generar emergencias
        for i in range(5):
            emergency = self.simulator.generate_random_emergency()
        
        print(f"Emergencias generadas: {len(self.simulator.emergencies)}")
        
        # Simular fallos múltiples
        failed_nodes = ["N2", "N4"]
        for node_id in failed_nodes:
            self.simulator.simulate_node_failure(node_id)
            print(f"Nodo {node_id} falló")
        
        active_after_failures = sum(1 for node in self.simulator.nodes.values() if node.active)
        print(f"Nodos activos después de fallos: {active_after_failures}")
        
        # Procesar emergencias con nodos reducidos
        processed_with_failures = 0
        while self.simulator.emergencies and processed_with_failures < 3:
            emergency, node, path = self.simulator.process_next_emergency()
            if emergency:
                processed_with_failures += 1
                print(f"Procesada emergencia {emergency.emergency_id} en nodo {node.node_id}")
        
        # Restaurar un nodo
        self.simulator.restore_node("N2")
        print("Nodo N2 restaurado")
        
        # Verificar que el nodo restaurado vuelve a estar disponible
        restored_node = self.simulator.nodes["N2"]
        self.assertTrue(restored_node.active)
        
        # Procesar emergencias restantes
        remaining_processed = 0
        while self.simulator.emergencies and remaining_processed < 2:
            emergency, node, path = self.simulator.process_next_emergency()
            if emergency:
                remaining_processed += 1
                print(f"Procesada emergencia {emergency.emergency_id} en nodo {node.node_id}")
        
        print(f"✓ Sistema se recuperó exitosamente de {len(failed_nodes)} fallos")

def run_performance_test():
    """Ejecuta una prueba de rendimiento adicional"""
    print("\n=== PRUEBA DE RENDIMIENTO EXTENDIDA ===")
    
    # Crear simulador grande
    simulator = LanSimulator()
    simulator.generate_random_topology(num_nodes=50, connection_density=0.3)
    
    # Generar muchas emergencias
    start_time = time.time()
    for _ in range(200):
        simulator.generate_random_emergency()
    
    # Procesar todas las emergencias
    processed = 0
    while simulator.emergencies:
        emergency, node, path = simulator.process_next_emergency()
        if emergency:
            processed += 1
        if processed >= 200:  # Evitar bucle infinito
            break
    
    total_time = time.time() - start_time
    
    print(f"Procesadas {processed} emergencias en {total_time:.2f} segundos")
    print(f"Rendimiento: {processed/total_time:.1f} emergencias/segundo")
    
    # Mostrar estadísticas finales
    stats = simulator.get_network_statistics()
    print(f"Estadísticas finales:")
    print(f"  - Emergencias completadas: {stats['completed_emergencies']}")
    print(f"  - Tiempo promedio de respuesta: {stats['avg_response_time']:.2f}s")
    print(f"  - Datos transmitidos: {stats['total_data_transmitted']} unidades")

if __name__ == "__main__":
    # Configurar el runner de pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    
    print("EJECUTANDO CASOS DE PRUEBA DEL SIMULADOR LAN")
    print("=" * 50)
    
    # Ejecutar pruebas sin mostrar los nombres individuales
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    result = runner.run(suite)
    
    # Ejecutar prueba de rendimiento adicional solo si las pruebas pasaron
    if result.wasSuccessful():
        run_performance_test()
        print("\n" + "=" * 50)
        print("TODAS LAS PRUEBAS COMPLETADAS")