# ======================================================================
#                      PROYECTO FINAL INTEGRADOR
# ======================================================================
# Archivo:   gestor_inventario.py
# Alumna:    Melisa S. Rossi
# Docente:   Gabriel Feldman
# Tutora:    Sofía Tarabusi
# Curso:     Iniciación a la Programación con Python
# Trayecto:  2024 - Talento Tech
# ----------------------------------------------------------------------
# Enunciado:
# Desarrollo de una aplicación Python para gestionar el inventario
# de una pequeña tienda. El sistema debe permitir registrar, actualizar,
# eliminar y mostrar productos. Además, incluirá funcionalidades para
# búsquedas y generación de reportes de productos con bajo stock.
# ======================================================================

# ➡️ Antes de utilizar el GESTOR DE INVENTARIO, es necesario correr el archivo inventario_db.py para su correcto funcionamiento. 

# Importar los módulos necesarios
import sqlite3 # Gestión de bases de datos SQLite.
import os # Interacción con el sistema operativo.
from colorama import init, Fore, Style, Back # Agregar colores y estilos al texto en la consola. ⚠️ Previamente instalarlo por consola: pip install colorama.
from tabulate import tabulate # Mostrar datos en forma de tabla. ⚠️ Previamente instalarlo por consola: pip install tabulate.

# Inicializar colorama para mejorar la interfaz de la terminal
init(autoreset=True)

# Variables de inicialización:
inventario = [] # Lista de productos. Claves: nombre, descripcion, cantidad, precio, categoria.
opcion = None # Necesario para WHILE de menú de opciones.
codigo_actual = 0 # Necesario para generar códigos de productos.

# Función para limpiar la pantalla:
def limpiar_pantalla():
    # Windows:
    if os.name == 'nt':
        os.system('cls')
    # Mac y Linux:
    else: 
        os.system('clear')

# Función que espera la presión de la tecla ENTER para continuar::
def esperar_enter():
    input(Style.BRIGHT + "➡️   PRESIONE " + Fore.BLUE + "ENTER " + Fore.WHITE + "PARA CONTINUAR")

# Función menú de opciones:
def mostrar_menu():
    print(Style.BRIGHT + Fore.GREEN + "\n☰ " + Fore.BLACK + " MENÚ DE GESTIÓN DE STOCK:\n")
    print("\t1. Registrar producto")
    print("\t2. Mostrar productos")
    print("\t3. Actualizar stock de un producto")
    print("\t4. Eliminar producto")
    print("\t5. Buscar producto")
    print("\t6. Reporte de bajo stock")
    print("\t7. Eliminar base de datos completa")
    print(Style.BRIGHT + Fore.RED + "\t8. Salir")

# Función para registrar un nuevo producto:
def registrar_producto():    
    # Conexión con la base de datos:
    conexion = sqlite3.connect("inventario_msr.db")
    cursor = conexion.cursor()   
    # Variable de inicialización:
    agregar = "s"
    # Bucle while que permite agregar productos hasta que el usuario indique lo contario escribiendo "n":
    while agregar.lower() == "s":
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}\n📋 Ingrese los datos para el producto:")
        nombre = input("   • Nombre: ").strip() 
        descripcion = input("   • Descripcion: ").strip()          
        # Bucle while para verificar que se ingrese un número de stock correcto (mayor o igual a 0):
        cantidad = -1
        while cantidad <= 0:
            cantidad = int(input("   • Cantidad en stock: "))
            if cantidad <= 0:
                print(f'   • {Style.BRIGHT}{Fore.RED}ERROR: La cantidad en stock no puede ser menor o igual a 0.')
        precio = -1.0
        # Bucle while para verificar que se ingrese un precio unitario correcto (mayor o igual a 0):
        while precio <= 0:
            precio = float(input("   • Precio unitario: $"))
            if precio <= 0:
                print(f'   • {Style.BRIGHT}{Fore.RED}ERROR: El precio no puede ser menor o igual a 0.')
        categoria = input("   • Categoría: ").strip() 
        # Ejecutar sentencia INSERT de SQL para agregar el producto a la tabla productos:
        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)", 
                       (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        # Obtener el ID del producto recién insertado:
        producto_id = cursor.lastrowid
        # Recuperar los datos del producto recién insertado usando el ID generado por SQLite:
        cursor.execute("SELECT * FROM productos WHERE ID = ?", (producto_id,))
        producto = cursor.fetchone()
        if producto:
            encabezado = ["ID", "NOMBRE", "DESCRIPCIÓN", "CANTIDAD", "PRECIO", "CATEGORÍA"]
            print(Style.BRIGHT + Fore.GREEN + "\n✅   Producto agregado correctamente:\n")
            print(tabulate([producto], headers=encabezado, tablefmt="rounded_grid", colalign=("center", "center", "center", "center", "center", "center")))
        else:
            print(f'{Style.BRIGHT}{Fore.RED}ERROR: No se pudo recuperar el producto recién agregado.')    
        # Preguntar para seguir ingresando productos o terminar el bucle while y volver al menú de opciones:           
        agregar = input(f'{Style.BRIGHT}\n¿Desea agregar otro producto?{Fore.GREEN} (s/n){Fore.WHITE}: ').strip().lower()
        print("")
    conexion.close()

# Función para mostrar productos:
def mostrar_productos():        
    # Conexión con la base de datos:
    conexion = sqlite3.connect("inventario_msr.db")
    cursor = conexion.cursor()
    # Ejecutar sentencia SELECT de SQL para mostrar todas las filas y columnas de la tabla de productos:
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    # Verificación usando un condicional para mostrar la lista de productos guardados:
    if not resultados:
        print(f'{Style.BRIGHT}{Fore.RED}⚠️   ERROR: No hay productos en el inventario.\n')
    else:
        encabezado = [
            f"{Fore.BLUE}{col}{Style.RESET_ALL}" 
            for col in ["ID", "NOMBRE", "DESCRIPCIÓN", "CANTIDAD", "PRECIO", "CATEGORÍA"]
        ]
        print("\n📋 Lista de productos:\n")
        print(tabulate(resultados, headers=encabezado, tablefmt="rounded_grid", colalign=("center", "center", "center", "center", "center", "center")))   
        print("")
    conexion.close()

# Función de actualizar la cantidad de un producto por ID: 
def actualizar_producto():
    # Llamar a la función mostrar_productos() para que el usuario vea los productos registrados:
    mostrar_productos()        
    # Conexión con la base de datos:
    conexion = sqlite3.connect("inventario_msr.db")
    cursor = conexion.cursor() 
    # Verificación de que haya productos en el inventario para continuar con la función:
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    if resultados:   
        # Solicitar ID del producto
        id = int(input(f'🆔   Ingrese el {Fore.MAGENTA}{Style.BRIGHT}ID{Fore.RESET}{Style.RESET_ALL} del producto cuya cantidad desea modificar: '))          
        # Verificar si el producto con el ID existe
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        producto = cursor.fetchone()    
        if producto:  
            # Solicitar nueva cantidad
            nueva_cantidad = int(input(f'\n🔢   Ingrese la nueva cantidad: '))
            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id))
            conexion.commit() 
            print(f'\n{Style.BRIGHT}{Fore.GREEN}✅   La cantidad fue modificada correctamente:\n')
            # Imprimir en pantalla los datos del producto modificado:
            cursor.execute("SELECT id, nombre, cantidad FROM productos WHERE id = ?", (id,))
            modificado = cursor.fetchall()
            encabezado = [
            f"{Fore.BLUE}{col}{Style.RESET_ALL}" 
            for col in ["ID", "NOMBRE", "CANTIDAD"]
            ]
            print(tabulate(modificado, headers=encabezado, tablefmt="rounded_grid", colalign=("center", "center", "center")))   
            print("")
        else: 
            print(f'\n{Style.BRIGHT}{Fore.RED}⚠️   ERROR: Producto no encontrado.\n')
    conexion.close()

# Función para eliminar un producto por ID:
def eliminar_producto():
    # Llamar a la función mostrar_productos() para que el usuario vea los productos registrados:
    mostrar_productos()        
    # Conexión con la base de datos:
    conexion = sqlite3.connect("inventario_msr.db")
    cursor = conexion.cursor() 
    # Verificación de que haya productos en el inventario para continuar con la función:
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    if resultados:    
        # Solicitar ID del producto:
        id = int(input(f'🆔   Ingrese el {Fore.MAGENTA}{Style.BRIGHT}ID{Style.RESET_ALL} del producto que desea {Fore.RED}{Style.BRIGHT}eliminar{Style.RESET_ALL}: '))
        # Verificar si el producto con el ID existe:
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        producto = cursor.fetchone()    
        if producto:
            # Solicitud de confirmación:
            respuesta = input(f'{Style.RESET_ALL}\n🚨  ¿Está seguro que desea eliminar el producto {Fore.MAGENTA}{Style.BRIGHT}{id}{Style.RESET_ALL}? (s/n): ').strip().lower()
            if respuesta == "s":
                # Ejecutar sentencia DELETE de SQL  para eliminar el producto:
                cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
                print(f'\n{Style.BRIGHT}{Fore.GREEN}✅  El producto fue eliminado correctamente.\n')
                conexion.commit()
            else:
                print(f'\n{Style.BRIGHT}{Fore.RED}❌  La eliminación fue cancelada.\n')
        else: 
            print(f'\n{Style.BRIGHT}{Fore.RED}⚠️   ERROR: Producto no encontrado.\n')        
    conexion.close()

def buscar_producto():    
    # Conexión con la base de datos:
    conexion = sqlite3.connect("inventario_msr.db")
    cursor = conexion.cursor() 
    # Verificación de que haya productos en el inventario para continuar con la función:
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    if resultados:            
        # Solicitud del nombre del producto:    
        nombre = input(f'📦   Ingrese el {Fore.MAGENTA}{Style.BRIGHT}nombre{Style.RESET_ALL} del producto que desea buscar: ')
        nombre = f"%{nombre}%"
        cursor.execute("SELECT * FROM productos WHERE nombre like ?", (nombre,))    
        resultados = cursor.fetchall()
        if resultados:
            print("")
            encabezado = [
            f"{Fore.BLUE}{col}{Style.RESET_ALL}" 
            for col in ["ID", "NOMBRE", "DESCRIPCIÓN", "CANTIDAD", "PRECIO", "CATEGORÍA"]
            ]
            print(tabulate(resultados, headers=encabezado, tablefmt="rounded_grid", colalign=("center", "center", "center", "center", "center", "center")))   
            print("")
        else: 
            print(f'\n{Style.BRIGHT}{Fore.RED}⚠️   ERROR: Producto no encontrado.\n')
    else:
        print(f'{Style.BRIGHT}{Fore.RED}⚠️   ERROR: No hay productos en el inventario.\n')
    conexion.close()

# Función de alerta de bajo stock:
def reporte_bajo_stock():
    # Conexión con la base de datos:
    conexion = sqlite3.connect("inventario_msr.db")
    cursor = conexion.cursor()
    # Solicitud del límite de bajo stock para generar la alerta:    
    limite = input(f'✋   Ingrese el {Fore.MAGENTA}{Style.BRIGHT}límite{Style.RESET_ALL} de bajo stock: ')
    # Ejecutar sentencia SELECT de SQL con un filtro WHERE para que recupere los datos que sean menor o igual al límite:
    query = f'SELECT * FROM productos WHERE cantidad <= {limite}'
    cursor.execute(query)
    productos = cursor.fetchall()
    if productos:
        print("")
        encabezado = [
        f"{Fore.BLUE}{col}{Style.RESET_ALL}" 
        for col in ["ID", "NOMBRE", "DESCRIPCIÓN", "CANTIDAD", "PRECIO", "CATEGORÍA"]
        ]
        print(tabulate(productos, headers=encabezado, tablefmt="rounded_grid", colalign=("center", "center", "center", "center", "center", "center")))   
        print("")
    else:
        print(f'\n{Style.BRIGHT}{Fore.GREEN}✅   No hay productos con bajo stock.\n')
    conexion.close()

# Función para eliminar completamente la base de datos:
def eliminar_bbdd():
    # Conexión con la base de datos:
    conexion = sqlite3.connect("inventario_msr.db")
    cursor = conexion.cursor()
    # Solicitud de confirmación:
    respuesta = input(f'{Style.BRIGHT}{Fore.RED}🚨  ¿Está seguro que desea eliminar la base de datos? (s/n): ').strip().lower()
    if respuesta == "s":
        # Ejecutar sentencia DELETE de SQL para eliminar la base de datos:
        cursor.execute("DELETE FROM productos")
        # Resetear el contador autoincremental de ID:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'productos'")
        print(f'\n{Style.BRIGHT}{Fore.GREEN}✅  La base de datos ha sido eliminada correctamente.\n')
        conexion.commit()
    else:
        print(f'\n{Style.BRIGHT}{Fore.RED}❌  La eliminación fue cancelada.\n')    
    conexion.close()

# Mensaje de bienvenida:
titulo = f"{Fore.WHITE}{Back.BLUE}{Style.BRIGHT}        ¡BIENVENIDO AL GESTOR DE INVENTARIOS!        "
linea = f"{Fore.LIGHTBLACK_EX}{'=' * 53}"
contenido = [
    ["Desarrollado por:", "Melisa S. Rossi"],
    ["Versión:", "1.0"],
    ["Uso:", "Administración de inventarios"]
]
limpiar_pantalla()
print(linea)
print("\n" + titulo + "\n")
print(tabulate(contenido, tablefmt="rounded_grid", colalign=("center", "center")))
print("")
print(linea)
print("")
esperar_enter() # Esperar que el usuario oprima ENTER para ver el Menú.

# Cuerpo de la aplicación:
while opcion != 8:  
    limpiar_pantalla()  
    mostrar_menu() 
    # Solicitud de ingreso de una opción:
    opcion = int(input("\n👉  Seleccione una opción (1 - 7): "))
    # Mensaje de verificación de opción seleccionada:
    print(Style.BRIGHT + Fore.GREEN + f"\n✅  Opción {opcion} seleccionada.\n")
    if opcion == 1:
        # Registrar un producto:
        limpiar_pantalla()
        print(Style.BRIGHT + "\n🛒 " + Fore.BLACK + " REGISTRO DE PRODUCTOS\n")
        registrar_producto()
    elif opcion == 2:
        # Motrar los productos:
        limpiar_pantalla()
        print(Style.BRIGHT + "\n📦 " + Fore.BLACK + " INVENTARIO\n")
        mostrar_productos()
        esperar_enter() 
    elif opcion == 3:
        # Actualizar un producto:
        limpiar_pantalla()
        print(Style.BRIGHT + "\n📤 " + Fore.BLACK + " ACTUALIZAR STOCK\n")
        actualizar_producto()
        esperar_enter()
    elif opcion == 4:
        # Eliminar un producto:
        limpiar_pantalla()
        print(Style.BRIGHT + "\n❌ " + Fore.BLACK + " ELIMINAR UN PRODUCTO\n")
        eliminar_producto()
        esperar_enter()
    elif opcion == 5:
        limpiar_pantalla()
        print(Style.BRIGHT + "\n🔎 " + Fore.BLACK + " BUSCAR UN PRODUCTO POR ID\n")
        buscar_producto() 
        esperar_enter()
    elif opcion == 6:
        limpiar_pantalla()
        print(Style.BRIGHT + "\n🚨 " + Fore.BLACK + " REPORTE BAJO STOCK\n")
        reporte_bajo_stock()
        esperar_enter()
    elif opcion == 7:
        limpiar_pantalla()
        print(Style.BRIGHT + "\n⚠️ " + Fore.BLACK + " ELIMINAR BASE DE DATOS\n")
        eliminar_bbdd()
        esperar_enter()
    elif opcion == 8:
        # Mensaje de despedida:
        limpiar_pantalla()
        titulo = f"{Fore.WHITE}{Back.BLUE}{Style.BRIGHT}       ¡GRACIAS POR UTILIZAR EL GESTOR DE INVENTARIO!       "
        linea = f"{Fore.LIGHTBLACK_EX}{'=' * 60}"
        print(linea)
        print("\n" + titulo + "\n")
        print(f"      Desarrollado por: Melisa S. Rossi | Versión: 1.0")
        print("\n" + linea)
        print("\n      ¡Hasta la próxima! Que tengas un excelente día 😊\n")
    else:
        # Mensaje de error al ingresar una opción incorrecta:
        print("=" * 53)
        print(f"{Fore.RED}{Style.BRIGHT}\n⚠️   {Fore.RED}ERROR: {Fore.WHITE}Seleccione una opción válida entre {Fore.GREEN}1{Fore.WHITE} y {Fore.GREEN}8{Fore.WHITE}.\n")
        print("=" * 53)
        print("")
        esperar_enter()