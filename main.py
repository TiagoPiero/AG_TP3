#Problema del viajante
import os
from colorama import Fore, Style, init
from clases import pais

init()

#Funciones
def menu():
    while (True):
        print(Fore.RED + "__" * 20 + Style.RESET_ALL)
        print(Fore.RED + "MENU PRINCIPAL".center(40) + Style.RESET_ALL)
        print(Fore.RED + "——" * 20 + Style.RESET_ALL)
        print("1. Buscar ruta mínima desde origen")
        print("2. Buscar recorrido minimo con heuristico")
        print("3. Buscar recorrido minimo con genetico")
        print("4. Salir")
        option = int(input("Ingrese una opcion: "))
        if(validar_opcion(option)):
            break
    return option

def validar_opcion(option):
    if(option < 1 or option > 4):
        return False
    return True

def ingresar_capital(pais,opcionMenu):
    os.system('cls')
    for i in range(len(pais.ciudades)):
        print(i+1,'- '+pais.ciudades[i])
    while(True):
        opcion = int(input("Ingrese una ciudad (1-24): "))
        if(opcion > 0 and opcion < 25):
            os.system('cls')
            break
    pais.calcularDistanciaMinima(opcion-1,opcionMenu)

#programa principal
while(True):
    option = menu()
    paisInstance = pais.pais()
    if(option == 4):
        os.system('cls')
        break
    if(option == 1):
        ingresar_capital(paisInstance,option)
    if(option == 2):
        os.system('cls')
        paisInstance.calcularRecorridoMinimo(option)
    if(option == 3):
        os.system('cls')
        print("1. Algoritmo Genético Sin Elitismo")
        print("2. Algoritmo Genético Con Elitismo")
        print("3. Volver al Menu Principal")
        op = int(input("Ingrese una opcion: "))
        if (op>0 and op<4):
            if(op == 1):
                os.system('cls')
                paisInstance.calcularRutaMinimaGenetico(usar_elitismo=False)
            elif (op == 2):
                os.system('cls')
                paisInstance.calcularRutaMinimaGenetico(usar_elitismo=True)
            else:
                os.system('cls')
        else:
            print("Opcion inválida")