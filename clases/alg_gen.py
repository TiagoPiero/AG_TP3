import random


class AlgoritmoGenetico:
    def __init__(self, distancias, ciudades):
        self.distancias = distancias
        self.ciudades = ciudades
        
        # Parámetros por defecto
        self.tamanoPoblacion = 50
        self.cantidadCorridas = 200
        self.probabilidadMutacion = 0.05
        self.probabilidadCrossover = 0.75
        self.porcentajeElitismo = 0.20
        
    def crear_individuo(self):
        # Crea una permutación de números del 1 al 24
        cromosoma = list(range(24)) #de 0 a 23
        random.shuffle(cromosoma)
        return cromosoma
        
    def crear_poblacion_inicial(self):
        return [self.crear_individuo() for _ in range(self.tamanoPoblacion)]
        
    def calcular_fitness(self,individuo):
        # Calcula la distancia total del recorrido
        distancia_total = 0
        for i in range(len(individuo)-1):
            ciudad_actual = individuo[i]
            ciudad_siguiente = individuo[i + 1]
            distancia_total += float(self.distancias.iloc[ciudad_actual, ciudad_siguiente+1])
            
        # print("Sin retorno: ", distancia_total)
        retorno = float(self.distancias.iloc[individuo[-1], individuo[0]+1])
        # print("Retorno: ",retorno)
        
        distancia_total += retorno   # Agregar distancia de retorno al origen
        fitness = 1 / distancia_total
        
        print("Individuo:", individuo," - Distancia total: ", distancia_total," - Fitness: ",fitness)
        # print("Distancia total: ", distancia_total)
        # print("Fitness: ",fitness)  # A mayor fitness, mejor. (menor distancia)
        
        return fitness
        
    def seleccion_ruleta(self, poblacion, fitness_poblacion):
        fitness_total = sum(fitness_poblacion)  # Fitness_total es la ruleta completa
        valor_ruleta = random.uniform(0, fitness_total)  # Giro de ruleta
        suma_actual = 0
        for i, individuo in enumerate(poblacion):  # Se acumula hasta saber que individuo resultó seleccionado 
            suma_actual += fitness_poblacion[i]
            if suma_actual > valor_ruleta:
                return individuo.copy()  #copy para no hacer lio con las referencias
        return poblacion[-1].copy()  # En caso de problemas de redondeo    
        
    def crossover(self, padre1, padre2):
        if random.random() > self.probabilidadCrossover:  #No hay crossover
            print("no hay crossover")
            return padre1.copy(),padre2.copy()
        
        def cyclic_crossover(p1, p2): 
            n = len(p1)
            hijo = [-1] * n  # -1 representa posiciones no ocupadas
            elementos_usados = set()  # Conjunto para guardar las ciudades ya utilizadas
            
            # Empezamos con el primer elemento del padre1
            inicio = 0
            index = inicio
            
            # Primer ciclo
            while True:
                # Copiamos el elemento del padre1 al hijo
                hijo[index] = p1[index]
                elementos_usados.add(p1[index])
                # Encontramos el valor correspondiente en padre2
                valor = p2[index]
                # Buscamos dónde está ese valor en padre1
                index = p1.index(valor)
                # Si volvimos al inicio, terminamos el ciclo
                if index == inicio:
                    break
            # Rellenamos las posiciones restantes con elementos del padre2
            # que no hayan sido usados
            for i in range(n):
                if hijo[i] == -1:  # Posición vacía
                    if p2[i] not in elementos_usados:
                        hijo[i] = p2[i]
                        elementos_usados.add(p2[i])
                    else:
                        # Si el elemento de p2 ya está usado, buscamos el primer elemento disponible que no se haya usado
                        for elemento in range(n):
                            if elemento not in elementos_usados:
                                hijo[i] = elemento
                                elementos_usados.add(elemento)
                                break
            
            return hijo
        
        hijo1 = cyclic_crossover(padre1, padre2)
        hijo2 = cyclic_crossover(padre2, padre1)
        return hijo1,hijo2

    def mutacion(self, individuo):
        if random.random() < self.probabilidadMutacion:
            print("Hijo antes de mutar: ",individuo)
            i, j = random.sample(range(len(individuo)), 2) #seleccion de dos índices aleatorios distintos del individuo
            individuo[i], individuo[j] = individuo[j], individuo[i] # intercambio de los elementos en las posiciones i y j.

        else:
            print("no hay mutacion")
        return individuo   
    
    def verificar_validez_individuo(self,individuo):
        # Verifica que el individuo sea una permutación válida
        numeros = sorted(individuo)
        return numeros == list(range(24))
    
    def generar_nueva_poblacion(self, poblacion, fitness_poblacion, usar_elitismo=True):
        
        individuos_ordenados = sorted(zip(poblacion, fitness_poblacion), key=lambda x: x[1], reverse=True)
        
        if usar_elitismo:
            print("\n Individuos ordenados: ", individuos_ordenados)
            cantidad_elites = int(self.tamanoPoblacion * self.porcentajeElitismo)
            print("Cantidad elites: ",cantidad_elites)
            # Crear nueva población, comenzando con los individuos elites
            nueva_poblacion = [ind[0].copy() for ind in individuos_ordenados[:cantidad_elites]]
        
        else:
            nueva_poblacion = []
              
        print("Nueva poblacion antes de reproduccion: ",nueva_poblacion)
        print("------------")
        
        # Crear el resto de la población mediante selección, crossover y mutación
        while len(nueva_poblacion) < self.tamanoPoblacion:
            padre1 = self.seleccion_ruleta(poblacion, fitness_poblacion)
            padre2 = self.seleccion_ruleta(poblacion, fitness_poblacion)
            print("\nRULETA")
            print("Padre 1: ",padre1," - Padre 2: ",padre2)

            hijo1,hijo2 = self.crossover(padre1, padre2)
            print("--Crossover--")
            print("Hijo 1 crossover: ",hijo1)
            print("Hijo 2 crossover: ",hijo2)
            
            hijo1 = self.mutacion(hijo1)
            hijo2 = self.mutacion(hijo2)
            print("--Mutacion--")
            print("Hijo 1 mutado: ",hijo1)
            print("Hijo 2 mutado: ",hijo2)
            
            print("\nHIJO 1: ",hijo1)
            print("\nHIJO 2: ",hijo2)
            
            if self.verificar_validez_individuo(hijo1):
                nueva_poblacion.append(hijo1)
            if self.verificar_validez_individuo(hijo2):
                nueva_poblacion.append(hijo2)
                
        print("------------------------------------------")
        print("\n\nNueva poblacion post reproduccion: ")
        for individuo in nueva_poblacion:
            print(individuo)
        
        # Aseguramos que la nueva población mantenga el tamaño correcto
        poblacion = nueva_poblacion[:self.tamanoPoblacion]

        return poblacion, individuos_ordenados        
            
    def ejecutar(self, usar_elitismo=True):
        print(f"Iniciando algoritmo genético {'con' if usar_elitismo else 'sin'} elitismo")
        
        poblacion = self.crear_poblacion_inicial()
        print("--------------------------------------------------------------------")
        print("Población inicial: ")
        for  individuo in poblacion:
            print(individuo)
        print("--------------------------------------------------------------------")
        
        # Lista para almacenar el progreso del fitness
        historial_fitness = []
        # Lista para almacenar el progreso de las distancias
        historial_distancias = [] 
        
        for generacion in range(self.cantidadCorridas):
            print(f"\nGeneración {generacion + 1}")
            print("-" * 50)
            
            # Calcular fitness de la población
            fitness_poblacion = [self.calcular_fitness(ind) for ind in poblacion]
            
            # Generar nueva población
            nueva_poblacion, individuos_ordenados = self.generar_nueva_poblacion(poblacion, fitness_poblacion, usar_elitismo)
            
            poblacion = nueva_poblacion
                        
            # Actualizar mejor fitness
            mejor_fitness_actual = max(fitness_poblacion)
            historial_fitness.append(mejor_fitness_actual)
            historial_distancias.append(1/mejor_fitness_actual)
            
            print("\nHistorial distancias: ",historial_distancias)
            print("Historial fitness: ",historial_fitness)
            print(f"Generación {generacion+1}: Mejor distancia = {1/mejor_fitness_actual:.2f} km")
            print("---------------------------------------------------------------------------------------------------------")
            
        # Resultado final. Convertimos indices a nombres de ciudades
        mejor_ruta = [self.ciudades[i] for i in individuos_ordenados[0][0]]
        mejor_ruta.append(mejor_ruta[0])
        distancia_total = 1 / individuos_ordenados[0][1]
        
        return {
            'mejor_ruta': mejor_ruta,
            'distancia_total': distancia_total,
            'historial_fitness': historial_fitness,
            'historial_distancias': historial_distancias
        }
