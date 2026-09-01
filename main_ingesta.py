import pandas as pd
import geopandas as gpd
import json
from pymongo import MongoClient

# Configuración de conexión al contenedor local
URI_MONGO = 'mongodb://localhost:27017/'
NOMBRE_DB = 'Residencia'

def cargar_asea(db):
    print("\n--- Procesando ASEA ---")
    archivo = "ASEA_residuos_peligrosos.csv"
    df = pd.read_csv(archivo)
    df['generacion_estimada'] = df['generacion_estimada'].astype(float)
    df = df.where(pd.notnull(df), None)
    
    coleccion = db['asea_residuos']
    coleccion.drop()
    registros = df.to_dict(orient='records')
    coleccion.insert_many(registros)
    print(f"✅ Éxito: {len(registros)} registros insertados.")

def cargar_conagua_climatologicas(db):
    print("\n--- Procesando CONAGUA (Climatológicas) ---")
    archivo = "CONAGUA_estaciones_climatologicas.csv"
    df = pd.read_csv(archivo, encoding='latin-1')
    df.columns = df.columns.str.strip().str.replace('\n', ' ')
    df['Latitud'] = df['Latitud'].astype(float)
    df['Longitud'] = df['Longitud'].astype(float)
    df = df.where(pd.notnull(df), None)
    
    coleccion = db['conagua_climatologicas']
    coleccion.drop()
    registros = df.to_dict(orient='records')
    coleccion.insert_many(registros)
    print(f"✅ Éxito: {len(registros)} registros insertados.")

def cargar_conagua_hidrometricas(db):
    print("\n--- Procesando CONAGUA (Hidrométricas) ---")
    archivo = "CONAGUA_estaciones_hidrometricas.csv"
    df = pd.read_csv(archivo, encoding='latin-1')
    df = df.where(pd.notnull(df), None)
    
    coleccion = db['conagua_hidrometricas']
    coleccion.drop()
    registros = df.to_dict(orient='records')
    coleccion.insert_many(registros)
    print(f"✅ Éxito: {len(registros)} registros insertados.")

def cargar_conanp(db):
    print("\n--- Procesando CONANP ---")
    archivo = "CONANP_areas_conservacion.csv"
    df = pd.read_csv(archivo)
    df['vigencia_anio'] = df['vigencia_anio'].fillna('Indefinido')
    df['superficie_certificada_ha'] = df['superficie_certificada_ha'].astype(float)
    df = df.where(pd.notnull(df), None)
    
    coleccion = db['conanp_conservacion']
    coleccion.drop()
    registros = df.to_dict(orient='records')
    coleccion.insert_many(registros)
    print(f"✅ Éxito: {len(registros)} registros insertados.")

def cargar_sagarpa(db):
    print("\n--- Procesando SAGARPA ---")
    archivo = "SAGARPA_cierre_agricola_mun_2025.csv"
    df = pd.read_csv(archivo, encoding='latin-1', low_memory=False) 
    df = df.where(pd.notnull(df), None)
    
    coleccion = db['sagarpa_agricola']
    coleccion.drop()
    registros = df.to_dict(orient='records')
    coleccion.insert_many(registros)
    print(f"✅ Éxito: {len(registros)} registros insertados.")

def cargar_profepa(db):
    print("\n--- Procesando PROFEPA ---")
    archivo = "PROFEPA_acciones_inspeccion.csv"
    df = pd.read_csv(archivo, encoding='latin-1') 
    df = df.where(pd.notnull(df), None)
    
    coleccion = db['profepa_inspecciones']
    coleccion.drop()
    registros = df.to_dict(orient='records')
    coleccion.insert_many(registros)
    print(f"✅ Éxito: {len(registros)} registros insertados.")

def cargar_imta(db):
    print("\n--- Procesando IMTA ---")
    archivo = "IMTA_calidad_agua_2026.csv"
    df = pd.read_csv(archivo, encoding='latin-1') 
    df = df.where(pd.notnull(df), None)
    
    coleccion = db['imta_agua']
    coleccion.drop()
    registros = df.to_dict(orient='records')
    coleccion.insert_many(registros)
    print(f"✅ Éxito: {len(registros)} registros insertados.")

def cargar_conabio(db):
    print("\n--- Procesando CONABIO (Chunks) ---")
    archivo = "CONABIO_snib_ejemplares_2026.csv"
    coleccion = db['conabio_especies']
    coleccion.drop()
    
    chunksize = 10000
    total = 0
    for chunk in pd.read_csv(archivo, encoding='latin-1', chunksize=chunksize, low_memory=False):
        chunk = chunk.where(pd.notnull(chunk), None)
        registros = chunk.to_dict(orient='records')
        coleccion.insert_many(registros)
        total += len(registros)
        
    print(f"✅ Éxito: {total} registros insertados.")

def cargar_conafor(db):
    print("\n--- Procesando CONAFOR ---")
    archivo = "CONAFOR_manejo_forestal_2021.xlsx"
    try:
        # Se apunta a la pestaña correcta y se omiten las dos primeras filas
        df = pd.read_excel(archivo, sheet_name='No maderable', header=2) 
        
        # Conversión obligatoria de los encabezados a texto para que MongoDB los acepte
        df.columns = df.columns.astype(str)
        
        df = df.where(pd.notnull(df), None)
        
        coleccion = db['conafor_forestal']
        coleccion.drop()
        registros = df.to_dict(orient='records')
        
        if len(registros) > 0:
            coleccion.insert_many(registros)
            print(f"✅ Éxito: {len(registros)} registros insertados.")
        else:
            print("⚠️ Advertencia: El archivo se leyó pero está vacío (0 registros).")
            
    except Exception as e:
        print(f"❌ Error al leer CONAFOR: {e}")

def cargar_semarnat(db):
    print("\n--- Procesando SEMARNAT ---")
    archivo = "SEMARNAT_sinaica_calidad_aire_2026_2027.csv"
    try:
        df = pd.read_csv(archivo, encoding='latin-1') 
        df = df.where(pd.notnull(df), None)
        
        coleccion = db['semarnat_aire']
        coleccion.drop()
        registros = df.to_dict(orient='records')
        
        if len(registros) > 0:
            coleccion.insert_many(registros)
            print(f"✅ Éxito: {len(registros)} registros insertados.")
        else:
            print("⚠️ Advertencia: El archivo se leyó pero está vacío (0 registros).")
            
    except Exception as e:
        print(f"❌ Error al leer SEMARNAT: {e}")

def cargar_inegi(db):
    print("\n--- Procesando INEGI (Mapas de Uso de Suelo) ---")
    archivo = "INEGI_uso_suelo_serieV/f1401_usv250s5a.shp" 
    
    try:
        gdf = gpd.read_file(archivo)
        gdf = gdf.to_crs(epsg=4326) 
        
        registros = []
        for _, fila in gdf.iterrows():
            propiedades = fila.drop('geometry').to_dict()
            geometria = json.loads(gpd.GeoSeries([fila['geometry']]).to_json())['features'][0]['geometry']
            
            documento = {
                "propiedades": propiedades,
                "geometria": geometria
            }
            registros.append(documento)
            
        coleccion = db['inegi_usosuelo']
        coleccion.drop()
        coleccion.insert_many(registros)
        print(f"✅ Éxito: {len(registros)} polígonos espaciales insertados.")
    except Exception as e:
        print(f"⚠️ Revisa la ruta exacta del archivo .shp dentro de tu carpeta INEGI. Detalle: {e}")

def ejecutar_pipeline():
    print("========================================================")
    print("Iniciando Orquestador ETL - Residencia Profesional")
    print("========================================================")
    print("Archivos programados para lectura en este flujo:")
    print("  1. ASEA_residuos_peligrosos.csv")
    print("  2. CONAGUA_estaciones_climatologicas.csv")
    print("  3. CONAGUA_estaciones_hidrometricas.csv")
    print("  4. CONANP_areas_conservacion.csv")
    print("  5. SAGARPA_cierre_agricola_mun_2025.csv")
    print("  6. PROFEPA_acciones_inspeccion.csv")
    print("  7. IMTA_calidad_agua_2026.csv")
    print("  8. CONABIO_snib_ejemplares_2026.csv")
    print("  9. CONAFOR_manejo_forestal_2021.xlsx")
    print(" 10. SEMARNAT_sinaica_calidad_aire_2026_2027.csv")
    print(" 11. INEGI_uso_suelo_serieV (Directorio Geoespacial)")
    print("========================================================\n")
    
    try:
        cliente = MongoClient(URI_MONGO)
        db = cliente[NOMBRE_DB]
        
        cargar_asea(db)
        cargar_conagua_climatologicas(db)
        cargar_conagua_hidrometricas(db)
        cargar_conanp(db)
        cargar_sagarpa(db)
        cargar_profepa(db)
        cargar_imta(db)
        cargar_conabio(db)
        cargar_conafor(db)
        cargar_semarnat(db)
        cargar_inegi(db)
        
        print("\n🚀 ¡PIPELINE ETL COMPLETADO AL 100%! 🚀")
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")

if __name__ == '__main__':
    ejecutar_pipeline()