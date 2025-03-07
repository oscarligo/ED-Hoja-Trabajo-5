import simpy
import random
import numpy as np

# Configuración de la simulación
RANDOM_SEED = 42  # Semilla para la generación de números aleatorios
random.seed(RANDOM_SEED)  # Inicializar la semilla

# Parámetros de la simulación
MEMORIA_RAM = 100  # Capacidad total de memoria RAM
VELOCIDAD_CPU = 3  # Instrucciones ejecutadas por unidad de tiempo
INTERVALO_LLEGADA = 10  # Intervalo de llegada de procesos (distribución exponencial)
NUM_PROCESOS = 5  # Número de procesos a simular (puedes cambiarlo manualmente)

# Crear el entorno de simulación
env = simpy.Environment()

# Definir recursos
RAM = simpy.Container(env, init=MEMORIA_RAM, capacity=MEMORIA_RAM)  # Memoria RAM
CPU = simpy.Resource(env, capacity=1)  # CPU con capacidad 1

# Función que modela el ciclo de vida de un proceso
def proceso(env, nombre, RAM, CPU):
    """
    Simula el ciclo de vida de un proceso en el sistema operativo.
    """
    tiempo_llegada = env.now  # Registrar el tiempo de llegada del proceso

    # Solicitar memoria
    memoria_necesaria = random.randint(1, 10)
    yield RAM.get(memoria_necesaria)  # Esperar hasta que haya suficiente memoria disponible

    # Pasar a ready y esperar CPU
    with CPU.request() as req:  # Solicitar el CPU
        yield req  # Esperar hasta que el CPU esté disponible

        # Ejecutar instrucciones
        instrucciones_totales = random.randint(1, 10)  # Número total de instrucciones a ejecutar
        print("memoria necesaria paso por running",instrucciones_totales)
        while instrucciones_totales > 0:  # Mientras queden instrucciones por ejecutar
            instrucciones_ejecutadas = min(VELOCIDAD_CPU, instrucciones_totales)  # Ejecutar hasta 3 instrucciones por unidad de tiempo
            yield env.timeout(1)  # Simular el tiempo de ejecución (1 unidad de tiempo)
            instrucciones_totales = instrucciones_totales-instrucciones_ejecutadas  # Actualizar el número de instrucciones restantes
            print("memoria necesaria paso despues running",instrucciones_totales)

            # Decidir si el proceso pasa a waiting o ready
            if instrucciones_totales > 0:  # Si aún quedan instrucciones por ejecutar
                decision = random.randint(1, 2)  # Decisión aleatoria: 1 = waiting, 2 = ready
                if decision == 1:  # Pasar a waiting (operaciones de I/O)
                    yield env.timeout(random.randint(1, 2))  # Simular el tiempo de I/O
                    print("memoria necesaria waiting",instrucciones_totales)

        # Liberar memoria
        yield RAM.put(memoria_necesaria)  # Devolver la memoria al sistema

    # Calcular y mostrar el tiempo total del proceso
    tiempo_total = env.now - tiempo_llegada  # Tiempo total en el sistema
    print(f"{nombre} completado. Tiempo total en el sistema: {tiempo_total} unidades de tiempo.")

# Función para generar procesos
def generador_procesos(env, RAM, CPU, num_procesos, intervalo_llegada):
    """
    Genera procesos en el sistema siguiendo una distribución exponencial.
    """
    for i in range(num_procesos):  # Generar el número especificado de procesos
        env.process(proceso(env, f"Proceso {i}", RAM, CPU))  # Crear un nuevo proceso
        yield env.timeout(random.expovariate(1.0 / intervalo_llegada))  # Esperar un tiempo aleatorio (distribución exponencial)

# Función para ejecutar la simulación
def ejecutar_simulacion(num_procesos, intervalo_llegada):
    """
    Ejecuta la simulación con los parámetros especificados.
    """
    # Iniciar la simulación
    env.process(generador_procesos(env, RAM, CPU, num_procesos, intervalo_llegada))  # Iniciar el generador de procesos
    env.run()  # Ejecutar la simulación hasta que todos los procesos hayan terminado

# Ejecutar la simulación
ejecutar_simulacion(NUM_PROCESOS, INTERVALO_LLEGADA)
