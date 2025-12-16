import os
import sys
import json
import time
import boto3
from pathlib import Path
from tqdm import tqdm

print("="*60)
print("GENERADOR DE AUDIOS - F5-TTS + R2")
print("="*60)

from f5_tts.api import F5TTS
import torch

print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

# Configuración
MANIFEST_FILE = "bible_verse_manifest.json"
PROGRESS_FILE = "generation_progress.json"
TEMP_AUDIO_DIR = "temp_audio"
REF_AUDIO_FILE = "reference_voice.wav"
REF_TEXT = "In the beginning God created the heaven and the earth. And the earth was without form and void."

R2_BUCKET = os.getenv("R2_BUCKET", "yourbible-audio")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")

if not all([R2_ACCESS_KEY, R2_SECRET_KEY, R2_ENDPOINT]):
    print("ERROR: Faltan variables de R2")
    sys.exit(1)

Path(TEMP_AUDIO_DIR).mkdir(exist_ok=True)

# Conectar R2
s3_client = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name='auto'
)

try:
    s3_client.head_bucket(Bucket=R2_BUCKET)
    print(f"Conectado a R2: {R2_BUCKET}")
except Exception as e:
    print(f"Error R2: {e}")
    sys.exit(1)

# Cargar manifest
with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
    verses = json.load(f)
print(f"Cargados {len(verses):,} versiculos")

# Cargar progreso
processed_verses = set()
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'r') as f:
        progress = json.load(f)
        processed_verses = set(progress.get('completed', []))
    print(f"Ya procesados: {len(processed_verses):,}")

pending_verses = [v for v in verses if v['r2_key'] not in processed_verses]
print(f"Pendientes: {len(pending_verses):,}\n")

if not pending_verses:
    print("Todo completado!")
    sys.exit(0)

# Verificar audio de referencia
if not os.path.exists(REF_AUDIO_FILE):
    print(f"ERROR: No se encuentra {REF_AUDIO_FILE}")
    print("Por favor descarga o sube un archivo de audio de referencia")
    sys.exit(1)

print(f"Usando audio de referencia: {REF_AUDIO_FILE}")

# Inicializar TTS
print("Inicializando F5-TTS...")
tts = F5TTS()
print("Modelo listo")

def generate_audio(text, output_path):
    """Genera audio usando F5-TTS con voz de referencia"""
    try:
        # <CHANGE> Llamar infer() que procesa y guarda internamente
        tts.infer(
            ref_file=REF_AUDIO_FILE,
            ref_text=REF_TEXT,
            gen_text=text,
            remove_silence=False,
            speed=0.75,
            # <CHANGE> Pasar file_wave directamente en infer()
            file_wave=output_path
        )
        
        return True
    except Exception as e:
        print(f"\nError generando: {e}")
        return False

def upload_to_r2(local_path, r2_key):
    """Sube a R2"""
    try:
        s3_client.upload_file(
            local_path,
            R2_BUCKET,
            r2_key,
            ExtraArgs={'ContentType': 'audio/mpeg'}
        )
        return True
    except Exception as e:
        print(f"\nError upload: {e}")
        return False

def save_progress():
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({
            'completed': list(processed_verses),
            'total': len(processed_verses),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=2)

print("\n" + "="*60)
print("INICIANDO GENERACION")
print("="*60 + "\n")

start_time = time.time()
errors = []

for idx, verse_data in enumerate(tqdm(pending_verses, desc="Generando"), 1):
    book = verse_data['book']
    chapter = verse_data['chapter']
    verse_num = verse_data['verse']
    text = verse_data['text']
    r2_key = verse_data['r2_key']
    
    temp_file = os.path.join(TEMP_AUDIO_DIR, f"{book}_c{chapter}_v{verse_num}.wav")
    
    if generate_audio(text, temp_file):
        if upload_to_r2(temp_file, r2_key):
            processed_verses.add(r2_key)
            os.remove(temp_file)
        else:
            errors.append({'verse': f"{book} {chapter}:{verse_num}", 'error': 'upload_failed'})
    else:
        errors.append({'verse': f"{book} {chapter}:{verse_num}", 'error': 'generation_failed'})
    
    if idx % 100 == 0:
        save_progress()
        elapsed = time.time() - start_time
        rate = idx / elapsed
        remaining = (len(pending_verses) - idx) / rate
        print(f"\n{idx}/{len(pending_verses)} | {rate:.2f} v/s | ETA: {remaining/3600:.1f}h")

save_progress()

print(f"\n{'='*60}")
print("COMPLETADO")
print(f"{'='*60}")
print(f"Procesados: {len(processed_verses):,}")
print(f"Errores: {len(errors)}")
print(f"Tiempo: {(time.time() - start_time)/3600:.2f}h")

if errors:
    with open('errors.json', 'w') as f:
        json.dump(errors, f, indent=2)