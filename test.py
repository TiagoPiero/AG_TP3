def crossover_ciclico(padre1, padre2):
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    n = len(padre1)
    hijo = [-1] * n  # -1 representa posiciones no llenadas
    
    # Comenzamos con el primer ciclo
    pos_actual = 0
    valor_actual = padre1[0]
    
    while True:
        # Copiamos el valor del padre1 al hijo
        hijo[pos_actual] = valor_actual
        
        # Encontramos el valor correspondiente en padre2
        valor_padre2 = padre2[pos_actual]
        
        # Si este valor ya está en la primera posición, terminamos el ciclo
        if valor_padre2 == padre1[0]:
            break
            
        # Buscamos la posición del valor_padre2 en padre1
        pos_actual = padre1.index(valor_padre2)
        valor_actual = padre1[pos_actual]
    
    # Llenamos las posiciones restantes con valores del padre2
    for i in range(n):
        if hijo[i] == -1:
            hijo[i] = padre2[i]
    
    return hijo

# Ejemplo de uso
padre1 = [8, 5, 7, 3, 6, 2, 4, 1, 9]
padre2 = [9, 8, 1, 7, 3, 2, 5, 6, 4]

hijo = crossover_ciclico(padre1, padre2)
print(f"Padre 1: {padre1}")
print(f"Padre 2: {padre2}")
print(f"Hijo:    {hijo}")