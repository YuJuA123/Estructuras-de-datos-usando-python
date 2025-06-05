"""
Simulador de Red LAN Inteligente para Respuesta a Emergencias
Proyecto Final - Redes Computacionales y Análisis de Algoritmos
"""

import heapq
import json
import random
import time
from collections import defaultdict
from math import inf

class LanNode:
    """Representa un nodo en la red LAN (estación de servicio o router)"""
    
    def __init__(self, node_id, name, node_type, location):
        """
        Inicializa un nodo LAN
        
        Args:
            node_id (str): Identificador único del nodo
            name (str): Nombre descriptivo del nodo
            node_type (str): Tipo de nodo (estación, router, etc.)
            location (tuple): Coordenadas (x, y) del nodo
        """
        self.node_id = node_id
        self.name = name
        self.node_type = node_type
        self.location = location
        self.resources = []  # Lista de recursos disponibles (ambulancias, bomberos, etc.)
        self.active = True  # Estado del nodo (activo/inactivo)
        self.stats = { #crea un diccionario que almacena estadisticas y metricas de rendimiento
            "data_transmitted": 0, #Cantidad total de datos transmitidos
            "incidents_handled": 0, #Numero de incidentes atendidos
            "response_times": [] #Lista de tiempos de respuesta para cada incidente
        }
    
    def add_resource(self, resource_type, count=1):
        """Agrega recursos al nodo, añade elementos al diccionario linea 30"""
        self.resources.append({"type": resource_type, "count": count})
    
    def has_resource(self, resource_type):
        """Verifica si el nodo tiene un recurso (quien atiende la emergencia) específico, lo revisa en el diccionario que esta en la linea 30"""
        for resource in self.resources:
            if resource["type"] == resource_type and resource["count"] > 0:
                return True
        return False
    
    def use_resource(self, resource_type):
        """Utiliza un recurso del nodo, linea 30"""
        for resource in self.resources:
            if resource["type"] == resource_type and resource["count"] > 0:
                resource["count"] -= 1
                return True
        return False
    
    def deactivate(self):
        """Desactiva el nodo (simulación de caída)"""
        self.active = False
    
    def activate(self):
        """Activa el nodo(cuando lo arreglan)"""
        self.active = True
    
    def update_stats(self, data_size, incident_handled=False, response_time=None):
        """Actualiza las estadísticas del nodo, referencia linea 32"""
        self.stats["data_transmitted"] += data_size
        if incident_handled:
            self.stats["incidents_handled"] += 1
        if response_time is not None:
            self.stats["response_times"].append(response_time)
    
    def get_avg_response_time(self):
        """Calcula el tiempo promedio de respuesta, la suma, sobre la cantidad"""
        if not self.stats["response_times"]:
            return 0
        return sum(self.stats["response_times"]) / len(self.stats["response_times"])
    
    def __str__(self):
        return f"Nodo {self.node_id}: {self.name} ({self.node_type})" #En un texto, escribe Nodo "id delcodigo": "Nombre del nodo" ("tipo de nodo")


class Emergency:
    """Representa una emergencia en el sistema"""
    
    # Definición de niveles de prioridad
    PRIORITY = {
        "ALTA": 3,
        "MEDIA": 2,
        "BAJA": 1
    }
    
    # Definición de tipos de emergencia y recursos necesarios
    EMERGENCY_TYPES = {
        "INCENDIO": {"priority": "ALTA", "resources": ["BOMBEROS"]},
        "ACCIDENTE_TRAFICO": {"priority": "ALTA", "resources": ["AMBULANCIA", "POLICIA"]},
        "ROBO": {"priority": "MEDIA", "resources": ["POLICIA"]},
        "INUNDACION": {"priority": "ALTA", "resources": ["BOMBEROS", "PROTECCION_CIVIL"]},
        "VANDALISMO": {"priority": "BAJA", "resources": ["POLICIA"]},
        "EMERGENCIA_MEDICA": {"priority": "ALTA", "resources": ["AMBULANCIA"]}
    }
    
    def __init__(self, emergency_id, emergency_type, location, timestamp=None):
        """
        Inicializa una emergencia
        
        Args:
            emergency_id (str): Identificador único de la emergencia
            emergency_type (str): Tipo de emergencia
            location (tuple): Coordenadas (x, y) de la emergencia
            timestamp (float): Marca de tiempo de la emergencia
        """
        self.emergency_id = emergency_id
        
        # Validar que el tipo de emergencia sea válido
        if emergency_type not in self.EMERGENCY_TYPES:
            raise ValueError(f"Tipo de emergencia no válido: {emergency_type}")
        
        self.emergency_type = emergency_type
        self.location = location
        self.timestamp = timestamp if timestamp else time.time() #Si comienza la emergencia, y no cuenta el tiempo entonces, inicia un time.time()
        self.status = "PENDIENTE"  # PENDIENTE, EN_PROGRESO, COMPLETADA
        self.assigned_node = None #El nodo aun no esta registrado
        self.resources_assigned = [] #Los recursos asignados
        
        # Asignar prioridad y recursos necesarios según el tipo
        self.priority = self.PRIORITY[self.EMERGENCY_TYPES[emergency_type]["priority"]]
        self.required_resources = self.EMERGENCY_TYPES[emergency_type]["resources"]
    
    def assign_to_node(self, node):
        """Asigna la emergencia a un nodo"""
        self.assigned_node = node
        self.status = "EN_PROGRESO"
    
    def complete(self):
        """Marca la emergencia como completada"""
        self.status = "COMPLETADA"
    
    def get_response_time(self):
        """Calcula el tiempo de respuesta"""
        return time.time() - self.timestamp
    
    def __lt__(self, other):
        """Permite comparar emergencias por prioridad (para la cola de prioridad)"""
        # Comparar primero por prioridad y luego por timestamp (más antiguo primero)
        if self.priority == other.priority:
            return self.timestamp < other.timestamp
        return self.priority > other.priority
    
    def __str__(self):
        return f"Emergencia {self.emergency_id}: {self.emergency_type} (Prioridad: {self.priority})"

class PathFinder:
    def __init__(self, nodes, connections):
        self.nodes = nodes
        self.connections = connections
    
    def euclidean_distance(self, loc1, loc2): #Hallar la distancia minima
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return (dx**2 + dy**2)**0.5
    
    def reconstruct_path(self, came_from, start, end):
        path = [] #Lista vacia que almacenara el camino
        current = end #Empieza desde el nodo final
        while current in came_from:
            path.append(current)
            current = came_from[current] #Va siguiendo hasta el start, o el nodo inicial
        path.append(start)
        path.reverse() #Revierte lo anterior
        return path
    
class LanSimulator:
    """Simulador principal de la red LAN"""
    
    def __init__(self):
        """Inicializa el simulador de red LAN"""
        self.nodes = {} # Diccionario de nodos (node_id -> LanNode)
        self.connections = defaultdict(list)  # Lista de adyacencia(grafos) para conexiones
        self.path_finder = PathFinder(self.nodes, self.connections)  # Nueva línea
        self.emergencies = []  # Cola de prioridad para emergencias
        self.emergency_registry = {}  # Registro de emergencias (emergency_id -> Emergency)
        self.zone_tree = {}  # Estructura para búsqueda por zonas
        self.stats = {
            "total_emergencies": 0,
            "completed_emergencies": 0,
            "avg_response_time": 0
        }
    
    def add_node(self, node):
        """
        Agrega un nodo a la red
        
        Args:
            node (LanNode): Nodo a agregar
        """
        self.nodes[node.node_id] = node
        # Inicializar la lista de adyacencia (GRafo) para este nodo
        if node.node_id not in self.connections:
            self.connections[node.node_id] = []
    
    def add_connection(self, node1_id, node2_id, weight):
        """
        Agrega una conexión entre dos nodos
        
        Args:
            node1_id (str): ID del primer nodo
            node2_id (str): ID del segundo nodo
            weight (float): Peso de la conexión (latencia/distancia)
        """
        # Verificar que ambos nodos existan
        if node1_id not in self.nodes or node2_id not in self.nodes:
            raise ValueError("Uno o ambos nodos no existen en la red")
        
        # Agregar la conexión en ambas direcciones (grafo no dirigido)
        self.connections[node1_id].append((node2_id, weight))
        self.connections[node2_id].append((node1_id, weight))
    
    def add_emergency(self, emergency):
        """
        Agrega una emergencia a la cola de prioridad
        
        Args:
            emergency (Emergency): Emergencia a agregar
        """
        heapq.heappush(self.emergencies, emergency) # cola que atiende por orden de prioridad
        self.emergency_registry[emergency.emergency_id] = emergency
        self.stats["total_emergencies"] += 1
        
        # Registrar en el árbol de zonas
        zone_key = self._get_zone_key(emergency.location) #convierte el lugar en el que ocurrio la emergencia en una clave unica
        if zone_key not in self.zone_tree: 
            self.zone_tree[zone_key] = []
        self.zone_tree[zone_key].append(emergency.emergency_id) #guarda en el diccionario
    
    def _get_zone_key(self, location):
        """
        Obtiene la clave de zona para una ubicación
        
        Args:
            location (tuple): Coordenadas (x, y)
        
        Returns:
            str: Clave de zona
        """
        # Dividir el espacio en cuadrantes de 10x10
        x, y = location
        return f"{int(x/10)}_{int(y/10)}"
    
    def get_emergencies_in_zone(self, zone_coords):
        """
        Obtiene las emergencias en una zona
        
        Args:
            zone_coords (tuple): Coordenadas de la zona
        
        Returns:
            list: Lista de emergencias en la zona
        """
        zone_key = self._get_zone_key(zone_coords) #Linea 236
        if zone_key not in self.zone_tree:
            return []
    
        return [self.emergency_registry[e_id] for e_id in self.zone_tree[zone_key] #Devuelve los detalles de las emergencias en las zonas, con sus identificadores
                if e_id in self.emergency_registry] #Si el identificador esta, lo recupera y lo añade a la lista
    
    def process_next_emergency(self):
        """
        Procesa la siguiente emergencia en la cola
        
        Returns:
            tuple: (emergencia procesada, nodo asignado, ruta)
        """
        if not self.emergencies:
            return None, None, None
        
        # Obtener la emergencia de mayor prioridad
        emergency = heapq.heappop(self.emergencies)
        
        # Encontrar el nodo más cercano con los recursos necesarios
        nearest_node, path = self._find_nearest_resource_node(
            emergency.location, 
            emergency.required_resources
        )
        
        if nearest_node:
            # Asignar la emergencia al nodo
            emergency.assign_to_node(nearest_node.node_id)
            
            # Actualizar estadísticas del nodo
            nearest_node.update_stats(
                data_size=100,  # Simulación de datos transmitidos
                incident_handled=True,
                response_time=emergency.get_response_time()
            )
            
            # Marcar la emergencia como completada
            emergency.complete()
            self.stats["completed_emergencies"] += 1
            
            # Actualizar tiempo promedio de respuesta
            total_times = sum([n.stats["response_times"] for n in self.nodes.values() if n.stats["response_times"]], [])
            if total_times:
                self.stats["avg_response_time"] = sum(total_times) / len(total_times)
            
            return emergency, nearest_node, path
        
        # Si no se encontró un nodo adecuado, volver a poner la emergencia en la cola
        heapq.heappush(self.emergencies, emergency)
        return None, None, None
    
    def _find_nearest_resource_node(self, location, required_resources):
        """Versión para encontrar la ruta mas cercana"""
        valid_nodes = [ # Se crea una tupla, en la que se cumplan las condiciones, de que el nodo este activo, y que tenga los recursos (ambulancias etc)
            (node_id, node) for node_id, node in self.nodes.items()
            if node.active and all(node.has_resource(r) for r in required_resources)
        ]
    
        if not valid_nodes:
            return None, None
        
        # Encontrar el nodo más cercano
        nearest_node_id, nearest_node = min(
            valid_nodes,
            key=lambda item: self.path_finder.euclidean_distance(item[1].location, location)
        )
    
        # Encontrar y validar nodo más cercano
        target_node_id = self._find_nearest_node_id(location)
        if not target_node_id:
            return None, None

        # Calcular ruta
        _, path = self.find_shortest_path(nearest_node_id, target_node_id)
        if not path:  # Si no hay camino
            return None, None
    
        return nearest_node, path

    def _find_nearest_node_id(self, location):
        """Helper para encontrar nodo más cercano a una ubicación"""
        active_nodes = [(node_id, node) for node_id, node in self.nodes.items() if node.active]
        if not active_nodes:
            return None #Filtra los nodos activos
        
        return min(
            active_nodes,
            key=lambda item: self.path_finder.euclidean_distance(item[1].location, location)
        )[0] #Encuentra el nodo a la menor distacia con la funcion euclidean
    
    def find_shortest_path(self, start_node_id, end_node_id):
        """Versión de Dijkstra(metodo que calcula la distancia mas corta) con heap(estructura que permite organizar los nodos en orden de prioridad)"""
        if start_node_id not in self.nodes or end_node_id not in self.nodes:
            raise ValueError("Uno o ambos nodos no existen en la red")

        # Inicialización
        distances = {node_id: inf for node_id in self.nodes}#inicializa todas las distancias en infinito
        distances[start_node_id] = 0 #La distancia del nodo inicial es 0
        previous_nodes = {node_id: None for node_id in self.nodes}#Almacena el nodo previo en el camino mas corto
        heap = [] #Estructura monticulo para manejar los nodos a evaluar
        heapq.heappush(heap, (0, start_node_id)) # Agrega el nodo inicial con distancia 0 al montículo.
    
        while heap:#Compara distancias, ignora las mas grandes
            current_dist, current_node = heapq.heappop(heap)
        
            if current_node == end_node_id: #Si llega al destino termina
                break
            
            if current_dist > distances[current_node]:
                continue
            #Busca el camino mas corto en una red de conexiones
            for neighbor, weight in self.connections[current_node]: #Compara las distancias entre los nodos, si la distancia es menor que la anterior se guarda
                if not self.nodes[neighbor].active:
                    continue
                
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(heap, (distance, neighbor))
    
        # Reconstrucción del camino
        path = []
        current = end_node_id
    
        if distances[end_node_id] == inf: #Si la ruta es innacesible regresa una ruta vacia
            return int, []
        
        while current:
            path.append(current) # Agrega cada nodo en el camino desde el destino hasta el inicio
            current = previous_nodes[current]
        
        path.reverse()#Para que vaya de inicio a destino
        return distances[end_node_id], path
    
    def simulate_node_failure(self, node_id):
        """
        Simula la falla de un nodo
        
        Args:
            node_id (str): ID del nodo que falla
        """
        if node_id not in self.nodes:
            raise ValueError(f"El nodo {node_id} no existe en la red")
        
        self.nodes[node_id].deactivate()
        print(f"El nodo {node_id} ha fallado. Recalculando rutas...")
    
    def restore_node(self, node_id):
        """
        Restaura un nodo que había fallado
        
        Args:
            node_id (str): ID del nodo a restaurar
        """
        if node_id not in self.nodes:
            raise ValueError(f"El nodo {node_id} no existe en la red")
        
        self.nodes[node_id].activate()
        print(f"El nodo {node_id} ha sido restaurado.")
    
    def load_topology_from_file(self, filename):
        """
        Carga la topología de la red desde un archivo JSON
        
        Args:
            filename (str): Ruta al archivo de topología
        """
        try:
            with open(filename, 'r') as file: #Abre el archivo como modo lectura
                data = json.load(file) #Convierte el contenido de data en un diccionario python
            
            # Cargar nodos
            for node_data in data.get("nodes", []):
                node = LanNode(
                    node_id=node_data["id"],
                    name=node_data["name"],
                    node_type=node_data["type"],
                    location=tuple(node_data["location"])
                )
                
                # Agregar recursos al nodo
                for resource in node_data.get("resources", []):
                    node.add_resource(resource["type"], resource["count"])
                
                self.add_node(node)
            
            # Cargar conexiones
            for connection in data.get("connections", []):
                self.add_connection(
                    connection["node1"], 
                    connection["node2"], 
                    connection["weight"]
                )
            
            print(f"Topología cargada correctamente desde {filename}")
            print(f"Nodos: {len(self.nodes)}, Conexiones: {sum(len(conns) for conns in self.connections.values()) // 2}")
        
        except Exception as e:
            print(f"Error al cargar la topología: {e}")
    
    def generate_random_topology(self, num_nodes=10, connection_density=0.3):
        """
        Genera una topología aleatoria
        
        Args:
            num_nodes (int): Número de nodos a generar
            connection_density (float): Densidad de conexiones (0-1)
        """
        # Tipos de nodos y recursos
        node_types = ["ESTACION", "ROUTER", "CENTRAL"]
        resource_types = ["AMBULANCIA", "BOMBEROS", "POLICIA", "PROTECCION_CIVIL"]
        
        # Generar nodos
        for i in range(num_nodes):
            node_id = f"N{i+1}"
            node_type = random.choice(node_types)
            location = (random.randint(0, 100), random.randint(0, 100))
            
            node = LanNode(
                node_id=node_id,
                name=f"Nodo {i+1}",
                node_type=node_type,
                location=location
            )
            
            # Agregar recursos aleatorios
            num_resources = random.randint(1, 3)
            for _ in range(num_resources):
                resource_type = random.choice(resource_types)
                count = random.randint(1, 5)
                node.add_resource(resource_type, count)
            
            self.add_node(node)
        
        # Generar conexiones
        node_ids = list(self.nodes.keys())
        max_connections = int(num_nodes * (num_nodes - 1) / 2 * connection_density)
        connections_made = 0
        
        # Asegurar que todos los nodos estén conectados (árbol de expansión)
        for i in range(1, num_nodes):
            node1 = f"N{i+1}"
            node2 = f"N{random.randint(1, i)}"
            weight = random.uniform(1, 10)
            self.add_connection(node1, node2, weight)
            connections_made += 1
        
        # Agregar conexiones adicionales según la densidad
        while connections_made < max_connections:
            node1 = random.choice(node_ids)
            node2 = random.choice(node_ids)
            
            # Evitar conexiones a sí mismo y conexiones duplicadas
            if node1 != node2 and not any(n == node2 for n, _ in self.connections[node1]):
                weight = random.uniform(1, 10)
                self.add_connection(node1, node2, weight)
                connections_made += 1
        
        print(f"Topología generada aleatoriamente con {num_nodes} nodos y {connections_made} conexiones")
    
    def generate_random_emergency(self):
        """
        Genera una emergencia aleatoria
        
        Returns:
            Emergency: Emergencia generada
        """
        emergency_id = f"E{self.stats['total_emergencies'] + 1}"
        emergency_type = random.choice(list(Emergency.EMERGENCY_TYPES.keys()))
        location = (random.randint(0, 100), random.randint(0, 100))
        
        emergency = Emergency(
            emergency_id=emergency_id,
            emergency_type=emergency_type,
            location=location
        )
        
        self.add_emergency(emergency)
        return emergency
    
    def get_network_statistics(self):
        """
        Obtiene estadísticas de la red
        
        Returns:
            dict: Estadísticas de la red
        """
        active_nodes = sum(1 for node in self.nodes.values() if node.active)
        total_data = sum(node.stats["data_transmitted"] for node in self.nodes.values())
        
        return {
            "total_nodes": len(self.nodes),
            "active_nodes": active_nodes,
            "total_emergencies": self.stats["total_emergencies"],
            "completed_emergencies": self.stats["completed_emergencies"],
            "pending_emergencies": len(self.emergencies),
            "avg_response_time": self.stats["avg_response_time"],
            "total_data_transmitted": total_data
        }
    
    def export_topology_to_graphviz(self, filename="topology.dot"):
        """
        Exporta la topología a formato Graphviz DOT
        
        Args:
            filename (str): Nombre del archivo de salida
        """
        with open(filename, 'w') as file: #Abre un archivo en modo escritura
            file.write("graph LAN {\n")#Define el tipo de grafo, no dirigido
            file.write("  node [shape=circle];\n") # Todos los nodos los deja en circulos
            
            # Escribir nodos
            for node_id, node in self.nodes.items():
                color = "green" if node.active else "red" #Color del nodo segun si esta activo o desactivado
                file.write(f'  "{node_id}" [label="{node.name}\\n{node.node_type}", color={color}];\n')
            
            # Escribir conexiones
            connections_added = set()
            for node1_id, connections in self.connections.items():
                for node2_id, weight in connections:
                    # Evitar duplicados, crea un set, si la conexion no ha sido agregada, la agrega con su peso
                    if (node1_id, node2_id) not in connections_added and (node2_id, node1_id) not in connections_added:
                        file.write(f'  "{node1_id}" -- "{node2_id}" [label="{weight:.2f}"];\n')
                        connections_added.add((node1_id, node2_id))
            
            file.write("}\n") #Cierra el archivo
        
        print(f"Topología exportada a {filename}")
        print("Para generar una imagen, ejecute: dot -Tpng topology.dot -o topology.png")


# Clase CLI para la interfaz de usuario
class LanSimulatorCLI:
    """Interfaz de línea de comandos para el simulador de red LAN"""
    
    def __init__(self):
        """Inicializa la interfaz CLI"""
        self.simulator = LanSimulator()
        self.running = False
    
    def show_menu(self):
        """Muestra el menú principal"""
        print("\n===== SIMULADOR DE RED LAN INTELIGENTE =====")
        print("1. Cargar topología desde archivo")
        print("2. Generar topología aleatoria")
        print("3. Agregar nodo")
        print("4. Agregar conexión")
        print("5. Simular emergencia aleatoria")
        print("6. Procesar la emergencia")
        print("7. Simular falla de nodo")
        print("8. Restaurar nodo")
        print("9. Mostrar estadísticas")
        print("10. Exportar topología a Graphviz")
        print("11. Simular múltiples emergencias")
        print("0. Salir")
        print("==========================================")
    
    def run(self):
        """Ejecuta la interfaz CLI"""
        self.running = True
        
        while self.running:
            self.show_menu()
            choice = input("Seleccione una opción: ")
            
            try:
                if choice == "1":
                    self.load_topology()
                elif choice == "2":
                    self.generate_topology()
                elif choice == "3":
                    self.add_node()
                elif choice == "4":
                    self.add_connection()
                elif choice == "5":
                    self.simulate_emergency()
                elif choice == "6":
                    self.process_emergency()
                elif choice == "7":
                    self.simulate_node_failure()
                elif choice == "8":
                    self.restore_node()
                elif choice == "9":
                    self.show_statistics()
                elif choice == "10":
                    self.export_topology()
                elif choice == "11":
                    self.simulate_multiple_emergencies()
                elif choice == "0":
                    self.running = False
                    print("¡Gracias por usar el simulador!")
                else:
                    print("Opción no válida. Intente de nuevo.")
            
            except Exception as e:
                print(f"Error: {e}")
    
    def load_topology(self):
        """Carga la topología desde un archivo"""
        filename = input("Ingrese el nombre del archivo de topología: ")
        self.simulator.load_topology_from_file(filename)
    
    def generate_topology(self):
        """Genera una topología aleatoria"""
        try:
            num_nodes = int(input("Ingrese el número de nodos: "))
            density = float(input("Ingrese la densidad de conexiones (0-1): "))
            self.simulator.generate_random_topology(num_nodes, density)
        except ValueError:
            print("Error: Ingrese valores numéricos válidos.")
    
    def add_node(self):
        """Agrega un nodo a la red"""
        try:
            node_id = input("Ingrese ID del nodo: ")
            name = input("Ingrese nombre del nodo: ")
            node_type = input("Ingrese tipo de nodo (ESTACION, ROUTER, CENTRAL): ")
            x = float(input("Ingrese coordenada X: "))
            y = float(input("Ingrese coordenada Y: "))
            
            node = LanNode(
                node_id=node_id,
                name=name,
                node_type=node_type,
                location=(x, y)
            )
            
            # Agregar recursos
            add_resources = input("¿Desea agregar recursos? (si/no): ").lower()== "si"
            while add_resources:
                resource_type = input("Tipo de recurso: ")
                count = int(input("Cantidad: "))
                node.add_resource(resource_type, count)
                
                add_resources = input("¿Agregar otro recurso? (si/no): ").lower() == "si"
            
            self.simulator.add_node(node)
            print(f"Nodo {node_id} agregado con éxito.")
        
        except ValueError:
            print("Error: Ingrese valores válidos.")
    
    def add_connection(self):
        """Agrega una conexión entre nodos"""
        try:
            node1_id = input("Ingrese ID del primer nodo: ")
            node2_id = input("Ingrese ID del segundo nodo: ")
            weight = float(input("Ingrese peso de la conexión: "))
            
            self.simulator.add_connection(node1_id, node2_id, weight)
            print(f"Conexión entre {node1_id} y {node2_id} agregada con éxito.")
        
        except ValueError:
            print("Error: Ingrese valores válidos.")
        except Exception as e:
            print(f"Error: {e}")
    
    def simulate_emergency(self):
        """Simula una emergencia aleatoria"""
        emergency = self.simulator.generate_random_emergency()
        print(f"Emergencia generada: {emergency}")
        print(f"Tipo: {emergency.emergency_type}")
        print(f"Ubicación: {emergency.location}")
        print(f"Prioridad: {emergency.priority}")
        print(f"Recursos requeridos: {emergency.required_resources}")
    
    def process_emergency(self):
        """Procesa la siguiente emergencia en la cola"""
        emergency, node, path = self.simulator.process_next_emergency()
        
        if emergency is None:
            print("No se pudo procesar la emergencia. No hay nodos disponibles con los recursos necesarios.")
            return
        
        print(f"Emergencia {emergency.emergency_id} procesada:")
        print(f"  - Asignada al nodo: {node.name} ({node.node_id})")
        print(f"  - Tiempo de respuesta: {emergency.get_response_time():.2f} segundos")
        print(f"  - Ruta calculada: {' -> '.join(path) if path else 'Directa'}")
    
    def simulate_node_failure(self):
        """Simula la falla de un nodo"""
        if not self.simulator.nodes:
            print("No hay nodos en la red para simular una falla.")
            return
        
        print("Nodos disponibles:")
        for node_id, node in self.simulator.nodes.items():
            status = "Activo" if node.active else "Inactivo"
            print(f"  - {node_id}: {node.name} ({status})")
        
        node_id = input("Ingrese el ID del nodo que fallará: ")
        try:
            self.simulator.simulate_node_failure(node_id)
        except ValueError as e:
            print(f"Error: {e}")
    
    def restore_node(self):
        """Restaura un nodo que había fallado"""
        if not self.simulator.nodes:
            print("No hay nodos en la red para restaurar.")
            return
        
        print("Nodos inactivos:")
        inactive_nodes = [(node_id, node) for node_id, node in self.simulator.nodes.items() if not node.active]
        
        if not inactive_nodes:
            print("No hay nodos inactivos para restaurar.")
            return
        
        for node_id, node in inactive_nodes:
            print(f"  - {node_id}: {node.name}")
        
        node_id = input("Ingrese el ID del nodo a restaurar: ")
        try:
            self.simulator.restore_node(node_id)
        except ValueError as e:
            print(f"Error: {e}")
    
    def show_statistics(self):
        """Muestra estadísticas de la red"""
        stats = self.simulator.get_network_statistics()
        
        print("\n===== ESTADÍSTICAS DE LA RED =====")
        print(f"Total de nodos: {stats['total_nodes']}")
        print(f"Nodos activos: {stats['active_nodes']}")
        print(f"Total de emergencias: {stats['total_emergencies']}")
        print(f"Emergencias completadas: {stats['completed_emergencies']}")
        print(f"Emergencias pendientes: {stats['pending_emergencies']}")
        print(f"Tiempo promedio de respuesta: {stats['avg_response_time']:.2f} segundos")
        print(f"Datos transmitidos: {stats['total_data_transmitted']} unidades")
        print("\nEstadísticas por nodo:")
        
        for node_id, node in self.simulator.nodes.items():
            status = "Activo" if node.active else "Inactivo"
            print(f"  - {node_id}: {node.name} ({status})")
            print(f"    * Datos transmitidos: {node.stats['data_transmitted']} unidades")
            print(f"    * Incidentes manejados: {node.stats['incidents_handled']}")
            if node.stats['response_times']:
                avg_time = sum(node.stats['response_times']) / len(node.stats['response_times'])
                print(f"    * Tiempo promedio de respuesta: {avg_time:.2f} segundos")
    
    def export_topology(self):
        """Exporta la topología a formato Graphviz"""
        filename = input("Ingrese el nombre del archivo de salida (por defecto: topology.dot): ") or "topology.dot"
        self.simulator.export_topology_to_graphviz(filename)
    
    def simulate_multiple_emergencies(self):
        """Simula múltiples emergencias y las procesa"""
        try:
            num_emergencies = int(input("Ingrese el número de emergencias a simular: "))
            
            print(f"Generando {num_emergencies} emergencias aleatorias...")
            for _ in range(num_emergencies):
                self.simulator.generate_random_emergency()
            
            process_all = input("¿Procesar todas las emergencias ahora? (si/no): ").lower() == "si"
            
            if process_all:
                print("\nProcesando emergencias...")
                processed = 0
                
                for _ in range(num_emergencies):
                    emergency, node, path = self.simulator.process_next_emergency()
                    if emergency:
                        processed += 1
                        print(f" - Emergencia {emergency.emergency_id} asignada a {node.name}")
                
                print(f"\nSe procesaron {processed} de {num_emergencies} emergencias.")
                if processed < num_emergencies:
                    print("Algunas emergencias no pudieron ser procesadas por falta de recursos.")
        
        except ValueError:
            print("Error: Ingrese un número válido de emergencias.")
            
    def find_path(self):
        node1 = input("ID del nodo origen: ")
        node2 = input("ID del nodo destino: ")
    
        # Simplificar ya que solo hay un algoritmo ahora
        dist, path = self.simulator.find_shortest_path(node1, node2)
        print(f"\nDistancia: {dist}")
        print(f"Camino: {' -> '.join(path) if path else 'No existe camino'}")
            
# Crear un ejemplo de archivo de topología
def create_example_topology_file(filename="example_topology.json"):
    """
    Crea un archivo de ejemplo de topología
    
    Args:
        filename (str): Nombre del archivo a crear
    """
    example_topology = {
        "nodes": [
            {
                "id": "N1",
                "name": "Estación Central",
                "type": "CENTRAL",
                "location": [50, 50],
                "resources": [
                    {"type": "AMBULANCIA", "count": 5},
                    {"type": "BOMBEROS", "count": 3},
                    {"type": "POLICIA", "count": 4}
                ]
            },
            {
                "id": "N2",
                "name": "Estación Norte",
                "type": "ESTACION",
                "location": [20, 80],
                "resources": [
                    {"type": "AMBULANCIA", "count": 2},
                    {"type": "POLICIA", "count": 3}
                ]
            },
            {
                "id": "N3",
                "name": "Estación Sur",
                "type": "ESTACION",
                "location": [80, 20],
                "resources": [
                    {"type": "BOMBEROS", "count": 3},
                    {"type": "PROTECCION_CIVIL", "count": 2}
                ]
            },
            {
                "id": "N4",
                "name": "Router Este",
                "type": "ROUTER",
                "location": [90, 50],
                "resources": []
            },
            {
                "id": "N5",
                "name": "Router Oeste",
                "type": "ROUTER",
                "location": [10, 50],
                "resources": []
            }
        ],
        "connections": [
            {"node1": "N1", "node2": "N2", "weight": 5.0},
            {"node1": "N1", "node2": "N3", "weight": 4.5},
            {"node1": "N1", "node2": "N4", "weight": 3.0},
            {"node1": "N1", "node2": "N5", "weight": 3.5},
            {"node1": "N2", "node2": "N5", "weight": 2.0},
            {"node1": "N3", "node2": "N4", "weight": 2.5}
        ]
    }
    
    with open(filename, 'w') as file: #Crea un archivo de lectura o lo sobreescribe
        json.dump(example_topology, file, indent=2) #Guarda los datos en formato json
    
    print(f"Archivo de ejemplo de topología creado: {filename}")


# Función principal
def main():
    """Función principal del programa"""
    # Crear archivo de ejemplo de topología
    create_example_topology_file()
    
    # Iniciar la interfaz CLI
    cli = LanSimulatorCLI()
    cli.run()


if __name__ == "__main__":
    main()