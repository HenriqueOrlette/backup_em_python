from invoke import task
import shutil
import os
from datetime import datetime
import zipfile

@task
def empacotar(c):
    # Criar um backup dos arquivos do projeto
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = f'backup_flask_{timestamp}.zip'
    incluir = ['app', 'src', 'template', 'tasks.py']

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in incluir:
            if os.path.exists(item):
                if os.path.isdir(item):
                    for root, _, files in os.walk(item):
                        for f in files:
                            path = os,path.join(root, f)
                            zipf.write(path, arcname=os.path.relpath(path))
                else:
                    zipf.write(item)
    print (f"Backup Criado: {zip_name}")

@task
def backup (c, source='.', destination='backup', dias_max=7):
    # Realiza backup e remove versões antigas
    # Args:
    #      dias_max (int) -> dias a manter backupd

    timestamp =datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_backup_dir = os.path.join(destination, f'temp_{timestamp}')
    zip_filename = os.path.join(destination, f'backup_flask_{timestamp}.zip')

    os.makedirs(temp_backup_dir, exist_ok=True)
    incluir = ['app', 'template', 'src', 'task.py']

    for item in incluir:
        if os.path.exists(item):
            destino_item = os.path.join(temp_backup_dir, item)
            try:
                if os.path.isdir(item):
                    shutil.copytree(item, destino_item)
                else:
                    shutil.copy2(item, destino_item)
                print(f'Copiado: {item}')
            except Exception as e:
                print(f'Erro ao copiar {item}: {e}')

    # Compactando arquivos...
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, temp_backup_dir))
        
    print(f'\n Backup criado em: {zip_filename}')