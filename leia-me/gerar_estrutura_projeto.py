import os

# Para gerar as dependencias explicitas: pipreqs . --force
# Para gerar a árvore de pastas: pip freeze > estrutura.txt

def gerar_estrutura_projeto(startpath, output_file, exclude_dirs=None):
    """
    Gera a estrutura de diretórios em formato de árvore
    :param startpath: Pasta raiz para iniciar a varredura
    :param output_file: Nome do arquivo de saída
    :param exclude_dirs: Lista de pastas para ignorar
    """
    if exclude_dirs is None:
        exclude_dirs = {'venv', '__pycache__', 'node_modules', '.git', '.idea'}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            # Filtra pastas a serem ignoradas
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            level = root.replace(startpath, '').count(os.sep)
            indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
            
            # Escreve o nome do diretório atual
            f.write(f"{indent}{os.path.basename(root)}/\n")
            
            # Escreve os arquivos
            subindent = '│   ' * level + '├── '
            for file in files:
                f.write(f"{subindent}{file}\n")

if __name__ == "__main__":
    # Lista de pastas para ignorar
    excluded = ['venv', '__pycache__', 'node_modules', '.git', '.vscode']
    
    gerar_estrutura_projeto(
        startpath='.',
        output_file='estrutura.txt',
        exclude_dirs=excluded
    )