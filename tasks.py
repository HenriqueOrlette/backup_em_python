from invoke import task
import shutil
import os
from datetime import datetime
import zipfile
import glob

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

@task
def descompactar(c, zip_file=None, destino='backup'):
    """
    Descompacta o arquivo zip no diretório de destino (dentro da pasta 'backup').
    Caso o zip_file não seja especificado, utiliza o último arquivo de backup encontrado.
    """
    # Defina a pasta de backups
    backup_folder = 'backup'  # A pasta onde os backups .zip são armazenados
    
    # Se zip_file não for fornecido, buscamos o último arquivo de backup criado dentro da pasta 'backup'
    if not zip_file:
        # Buscar os arquivos de backup na pasta 'backup' com o padrão de nome
        backups = glob.glob(os.path.join(backup_folder, "backup_flask_*.zip"))
        if backups:
            # Seleciona o mais recente usando a data de modificação
            zip_file = max(backups, key=os.path.getmtime)
            print(f"Usando o arquivo de backup mais recente: {zip_file}")
        else:
            print("Erro: Nenhum arquivo de backup encontrado na pasta 'backup'.")
            return
    
    if not os.path.exists(zip_file):
        print(f"Erro: O arquivo {zip_file} não existe.")
        return

    # Cria uma nova pasta para descompactação dentro da pasta 'backup', baseada no nome do arquivo de backup
    nome_backup = os.path.splitext(os.path.basename(zip_file))[0]
    destino_completo = os.path.join(backup_folder, nome_backup)  # Pasta dentro de 'backup'
    
    if not os.path.exists(destino_completo):
        os.makedirs(destino_completo)

    try:
        # Descompacta o arquivo zip na nova pasta dentro de 'backup'
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destino_completo)
        print(f'Backup descompactado com sucesso em: {destino_completo}')
    except zipfile.BadZipFile:
        print(f'Erro: O arquivo {zip_file} não é um arquivo zip válido.')
    except Exception as e:
        print(f'Erro ao descompactar o arquivo {zip_file}: {e}')

