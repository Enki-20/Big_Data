import happybase
import pandas as pd

try:
    # 1. Establecer conexión con HBase
    connection = happybase.Connection('localhost')
    print("Conexión establecida con HBase")

    # 2. Crear la tabla con las familias de columnas
    table_name = 'used_cars_analysis'
    families = {
        'basic': dict(),  # información básica del coche
        'specs': dict(),  # especificaciones técnicas
        'sales': dict(),  # información de venta
    }

    # Eliminar la tabla si ya existe
    if table_name.encode() in connection.tables():
        print(f"Eliminando tabla existente - {table_name}")
        connection.delete_table(table_name, disable=True)
    
    # Crear nueva tabla
    connection.create_table(table_name, families)
    table = connection.table(table_name)
    print(f"Tabla '{table_name}' creada exitosamente")

    # 3. Cargar datos del CSV
    car_data = pd.read_csv('Car_details_v3.csv')

    # Iterar sobre el DataFrame usando el índice
    for index, row in car_data.iterrows():
        # Generar row key basado en el índice
        row_key = f'car_{index}'.encode()

        # Organizar los datos en familias de columnas
        data = {
            b'basic:name': str(row['name']).encode(),
            b'basic:brand': str(row['name'].split(' ')[0]).encode(),  # Marca extraída del nombre
            b'basic:year': str(row['year']).encode(),

            b'specs:engine': str(row['engine']).encode(),
            b'specs:fuel': str(row['fuel']).encode(),
            b'specs:km_driven': str(row['km_driven']).encode(),

            b'sales:selling_price': str(row['selling_price']).encode(),
        }

        table.put(row_key, data)

    print("Datos cargados exitosamente")

    # 4. Consultas y análisis alternativos

    # a) Clasificación de coches por marca
    print("\n=== Clasificación de coches por marca ===")
    brand_count = {}
    for key, data in table.scan():
        brand = data[b'basic:brand'].decode()
        brand_count[brand] = brand_count.get(brand, 0) + 1
    
    for brand, count in sorted(brand_count.items(), key=lambda x: x[1], reverse=True)[:5]:  # Top 5 marcas
        print(f"Marca: {brand}, Cantidad: {count}")

    # b) Kilometraje promedio por tipo de combustible
    print("\n=== Kilometraje promedio por tipo de combustible ===")
    fuel_km = {}
    fuel_counts = {}

    for key, data in table.scan():
        fuel = data[b'specs:fuel'].decode()
        km_driven = int(data[b'specs:km_driven'].decode())

        fuel_km[fuel] = fuel_km.get(fuel, 0) + km_driven
        fuel_counts[fuel] = fuel_counts.get(fuel, 0) + 1
    
    for fuel in fuel_km:
        avg_km = fuel_km[fuel] / fuel_counts[fuel]
        print(f"Combustible: {fuel}, Kilometraje promedio: {avg_km:.2f} km")

    # c) Autos más recientes (por año)
    print("\n=== Autos más recientes (Top 5) ===")
    recent_cars = []

    for key, data in table.scan():
        recent_cars.append({
            'id': key.decode(),
            'name': data[b'basic:name'].decode(),
            'year': int(data[b'basic:year'].decode()),
            'price': int(data[b'sales:selling_price'].decode())
        })

    for car in sorted(recent_cars, key=lambda x: x['year'], reverse=True)[:5]:
        print(f"ID: {car['id']}, Nombre: {car['name']}, Año: {car['year']}, Precio: {car['price']}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    # Cerrar la conexión
    connection.close()
