"""
Script SIMPLIFICADO para subir archivos de lecciones a Cloudflare R2
Busca archivos en el mismo directorio que el script
"""

import os
import sys
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

print("=" * 60)
print("UPLOADER SIMPLIFICADO DE LECCIONES A R2")
print("=" * 60)

# Configuración R2
R2_BUCKET = "yourbible-lessons"
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")

if not all([R2_ACCESS_KEY, R2_SECRET_KEY, R2_ENDPOINT]):
    print("❌ ERROR: Faltan variables de entorno R2")
    print("   Configura estas variables antes de ejecutar:")
    print("   export R2_ACCESS_KEY='tu_key'")
    print("   export R2_SECRET_KEY='tu_secret'")
    print("   export R2_ENDPOINT='https://tu_id.r2.cloudflarestorage.com'")
    sys.exit(1)

# Conectar a R2
try:
    s3 = boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        region_name='auto'
    )
    
    # Verificar conexión
    s3.head_bucket(Bucket=R2_BUCKET)
    print(f"✅ Conectado a R2: {R2_BUCKET}")
    
except ClientError as e:
    print(f"❌ Error conectando a R2: {e}")
    print("\n💡 Soluciones:")
    print("1. Verifica que el bucket 'yourbible-lessons' existe")
    print("2. Verifica tus credenciales R2")
    print("3. Verifica el endpoint de R2")
    sys.exit(1)

def upload_file(file_path, book_name="main course"):
    """Sube un archivo a R2"""
    try:
        file_name = os.path.basename(file_path)
        
        # Detectar libro del nombre del archivo
        file_lower = file_name.lower()
        books = {
            "genesis": "genesis",
            "exodus": "exodus", 
            "leviticus": "leviticus",
            "numbers": "numbers",
            "deuteronomy": "deuteronomy"
        }
        
        detected_book = None
        for key, value in books.items():
            if key in file_lower:
                detected_book = value
                break
        
        if detected_book is None:
            detected_book = "unknown"
            print(f"⚠  No se pudo detectar el libro para: {file_name}")
            print(f"   Usando: {detected_book}")
        
        # Ruta en R2
        r2_path = f"main course/{detected_book}/{file_name}"
        
        # Subir archivo
        with open(file_path, 'rb') as f:
            s3.put_object(
                Bucket=R2_BUCKET,
                Key=r2_path,
                Body=f,
                ContentType='text/typescript'
            )
        
        file_size_kb = os.path.getsize(file_path) / 1024
        print(f"✅ Subido: {file_name}")
        print(f"   Ruta R2: {r2_path}")
        print(f"   Tamaño: {file_size_kb:.1f} KB")
        return True
        
    except Exception as e:
        print(f"❌ Error subiendo {file_path}: {e}")
        return False

def main():
    """Función principal"""
    # Directorio actual (donde está este script)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n📂 Directorio actual: {current_dir}")
    
    # Buscar archivos .ts
    ts_files = []
    for ext in [".ts", ".TS"]:
        ts_files.extend(list(Path(current_dir).glob(f"*{ext}")))
    
    if not ts_files:
        print("\n🔍 Buscando en directorio actual...")
        for item in os.listdir(current_dir):
            if item.lower().endswith('.ts'):
                ts_files.append(Path(current_dir) / item)
    
    if not ts_files:
        print("❌ No se encontraron archivos .ts en el directorio actual")
        print("\n💡 Coloca los archivos .ts en la misma carpeta que este script")
        return
    
    print(f"\n📄 Encontrados {len(ts_files)} archivos .ts:")
    for i, file in enumerate(ts_files, 1):
        print(f"   {i:2d}. {file.name}")
    
    # Preguntar al usuario
    print("\n" + "-"*60)
    choice = input("¿Subir TODOS estos archivos? (s/n): ").strip().lower()
    
    if choice != 's':
        print("❌ Operación cancelada")
        return
    
    print("\n" + "="*60)
    print("INICIANDO SUBIDA...")
    print("="*60)
    
    successful = 0
    failed = 0
    
    for file_path in ts_files:
        print(f"\n📤 Procesando: {file_path.name}")
        if upload_file(file_path):
            successful += 1
        else:
            failed += 1
    
    # Resultado final
    print("\n" + "="*60)
    print("RESUMEN DE SUBIDA:")
    print("="*60)
    
    if successful > 0:
        print(f"✅ Archivos subidos exitosamente: {successful}")
    
    if failed > 0:
        print(f"❌ Archivos con error: {failed}")
    
    if successful == 0:
        print("⚠  No se subió ningún archivo")
    
    print(f"\n📊 Total procesados: {len(ts_files)}")
    print("="*60)

if __name__ == "__main__":
    main()