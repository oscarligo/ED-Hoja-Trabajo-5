import simpy
import random
import statistics

# Josue Hernández - 24770 

# Gabriel Hidalgo – 24939 

# Oscar Rompich - 24880 

# Fecha: 26/08/2021



# Configuración de la simulación

random.seed(100)  # Semilla 
env = simpy.Environment() # Entorno de simulación
velocidad = 3 # Velocidad de procesamiento de la CPU
capacidad_ram=200 # Capacidad de la memoria RAM
procesadores = 1 # Cantidad de procesadores

ram = simpy.Container(env, init=capacidad_ram, capacity=capacidad_ram) 
cpu = simpy.Resource(env, capacity=procesadores) 


intervalo = 10  # Intervalo de tiempo de creación de procesos
num_procesos = 25  # Cantidad de procesos

tiempos_por_proceso = []  # Lista para almacenar el tiempo de ejecución de cada proceso

def ejecutar_programa(env, nombre, instrucciones, memoria_requerida):
    """Simula la ejecución de un proceso en la CPU con consumo de memoria."""

# Solicitar RAM
    with ram.get(memoria_requerida) as req:
        
        yield req

        # Tiempo de llegada del proceso

        tiempo_de_llegada = env.now

        #  Información cuando un proceso llega

        print(f"\n+++ ({env.now:.2f}) Se genera {nombre} y entra a READY | {instrucciones} instrucciones | {memoria_requerida}MB RAM usada\nRAM DISPONIBLE: {ram.level} MB\n")

        # Solicitar CPU
        while instrucciones > 0:
            with cpu.request() as req:
                yield req
                ejecucion = min(velocidad, instrucciones)  # Procesa 3 instrucciones o menos
                # Tiempo de ejecución
                yield env.timeout(1)
                instrucciones -= ejecucion

                # Información del proceso en ejecución
                
                print(f"### ({env.now:.2f} ) {nombre} entra a RUNNING y ejecuta {ejecucion} instrucciones | Quedan: {instrucciones}")

                # Ingreso a WAITING o  regreso a READY

                if (random.randint(1, 2) == 1 and instrucciones > 0):

                    yield env.timeout(1)  # Espera 1 segundo
                    print(f"--- {nombre} entra a WAITING en {env.now:.2f}")


        # Devolver RAM al finalizar ejecutar todas las intrucciones de un proceso
        yield ram.put(memoria_requerida)


        # Tiempo que tarda un proceso en completarse
        tiempo_por_proceso = env.now - tiempo_de_llegada

        # Información cuando un proceso termina
        print(f"\nXXX {nombre} TERMINADO en {tiempo_por_proceso:.2f} | RAM DISPONIBLE: {ram.level} MB\n")
        # Se añade el tiempo de ejecución a la lista con todos los tiempos
        tiempos_por_proceso.append(tiempo_por_proceso)



# Generar procesos con instricciones y memoria requerida aleatorias
def generar_procesos(env, num_procesos):
    """Genera procesos con tiempos de llegada aleatorios."""
    # Crear la cantidad de procesos especificada
    for i in range(1, num_procesos + 1):
        yield env.timeout(random.expovariate(1.0 / intervalo))  # Intervalo de creación de procesos
        instrucciones = random.randint(1, 10)  # Número aleatorio de instrucciones
        memoria_requerida = instrucciones  # Memoria requerida = número de instrucciones
        env.process(ejecutar_programa(env, f"Proceso {i}", instrucciones, memoria_requerida))

# Iniciar la simulación
env.process(generar_procesos(env, num_procesos))
env.run()


# Resultados de la simulación
print("\n====== Resultados de la simulación ======")
print(f"Tiempo promedio de ejecución: {statistics.mean(tiempos_por_proceso):.2f}")
print(f"Desviación estándar del tiempo de ejecución: {statistics.stdev(tiempos_por_proceso):.2f}")
print(f"Procesos completados: {len(tiempos_por_proceso)}")      

