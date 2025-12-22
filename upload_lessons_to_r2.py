"""
Script para subir archivos de lecciones a Cloudflare R2
Uso: python scripts/upload_lessons_to_r2.py
"""

import os
import sys
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

print("=" * 50)
print("UPLOADER DE LECCIONES A R2")
print("=" * 50)

# Configuración R2
R2_BUCKET = "yourbible-lessons"
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")

if not all([R2_ACCESS_KEY, R2_SECRET_KEY, R2_ENDPOINT]):
    print("ERROR: Faltan variables de entorno R2")
    print("Requeridas: R2_ACCESS_KEY, R2_SECRET_KEY, R2_ENDPOINT")
    sys.exit(1)

# Conectar a R2
try:
    s3_client = boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        region_name='auto'
    )
    
    s3_client.head_bucket(Bucket=R2_BUCKET)
    print(f"✓ Conectado a R2: {R2_BUCKET}\n")
except ClientError as e:
    print(f"✗ Error conectando a R2: {e}")
    sys.exit(1)

def upload_lesson_file(local_path, r2_key):
    """
    Sube un archivo de lección a R2
    
    Args:
        local_path: Ruta local del archivo
        r2_key: Ruta en R2 (ej: "main course/genesis/genesis-lessons-7-12.ts")
    
    Returns:
        bool: True si se subió exitosamente
    """
    try:
        with open(local_path, 'rb') as file:
            s3_client.put_object(
                Bucket=R2_BUCKET,
                Key=r2_key,
                Body=file,
                ContentType='text/typescript'
            )
        print(f"✓ Subido: {r2_key}")
        return True
    except Exception as e:
        print(f"✗ Error subiendo {r2_key}: {e}")
        return False

def upload_lessons_from_directory(local_dir, course_name="main course"):
    """
    Sube todos los archivos .ts de un directorio a R2
    
    Args:
        local_dir: Directorio local con los archivos de lecciones
        course_name: Nombre del curso (default: "main course")
    
    Returns:
        tuple: (exitosos, fallidos)
    """
    local_path = Path(local_dir)
    
    if not local_path.exists():
        print(f"✗ El directorio no existe: {local_dir}")
        return 0, 0
    
    # Buscar todos los archivos .ts
    lesson_files = list(local_path.glob("**/*.ts"))
    
    if not lesson_files:
        print(f"✗ No se encontraron archivos .ts en: {local_dir}")
        return 0, 0
    
    print(f"Encontrados {len(lesson_files)} archivos de lecciones\n")
    
    successful = 0
    failed = 0
    
    for lesson_file in lesson_files:
        # Determinar el libro desde el nombre del archivo
        # Ej: genesis-lessons-7-12.ts -> genesis
        file_name = lesson_file.name
        
        if file_name.startswith("genesis"):
            book = "genesis"
        elif file_name.startswith("exodus"):
            book = "exodus"
        elif file_name.startswith("leviticus"):
            book = "leviticus"
        elif file_name.startswith("numbers"):
            book = "numbers"
        elif file_name.startswith("deuteronomy"):
            book = "deuteronomy"
        else:
            # Intentar extraer el libro del nombre del archivo
            parts = file_name.split("-")
            book = parts[0] if parts else "unknown"
        
        # Construir la ruta en R2
        r2_key = f"{course_name}/{book}/{file_name}"
        
        if upload_lesson_file(lesson_file, r2_key):
            successful += 1
        else:
            failed += 1
    
    return successful, failed

def upload_single_file(local_file, book_name, course_name="main course"):
    """
    Sube un solo archivo de lección a R2
    
    Args:
        local_file: Ruta del archivo local
        book_name: Nombre del libro (ej: "genesis")
        course_name: Nombre del curso (default: "main course")
    
    Returns:
        bool: True si se subió exitosamente
    """
    local_path = Path(local_file)
    
    if not local_path.exists():
        print(f"✗ El archivo no existe: {local_file}")
        return False
    
    file_name = local_path.name
    r2_key = f"{course_name}/{book_name}/{file_name}"
    
    return upload_lesson_file(local_path, r2_key)

# Ejemplos de uso
if __name__ == "__main__":
    print("OPCIONES DE USO:")
    print("-" * 50)
    print()
    print("1. Subir un directorio completo:")
    print("   lessons_dir = 'path/to/lessons'")
    print("   successful, failed = upload_lessons_from_directory(lessons_dir)")
    print()
    print("2. Subir un archivo individual:")
    print("   upload_single_file('genesis-lessons-7-12.ts', 'genesis')")
    print()
    print("-" * 50)
    print()
    
    # EJEMPLO: Descomentar para subir archivos
    # successful, failed = upload_lessons_from_directory("./lessons")
    # print(f"\n✓ Exitosos: {successful}")
    # print(f"✗ Fallidos: {failed}")
