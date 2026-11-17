from pathlib import Path

def gerar_arvore_diretorio(diretorio_raiz):
    diretorio_raiz = Path(diretorio_raiz).resolve()
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
    arquivo_saida_nome = 'documento_final_scripts.txt'
    linhas_arvore = ['.']
    total_dirs = 0
    total_files = 0

    def _percorrer(pasta_atual, prefixo=''):
        nonlocal total_dirs, total_files
        try:
            entradas = sorted(list(pasta_atual.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
        except PermissionError:
            return
        entradas_validas = []
        for e in entradas:
            if e.name in pastas_ignoradas:
                continue
            if pasta_atual == diretorio_raiz and e.name == arquivo_saida_nome:
                continue
            entradas_validas.append(e)
        for i, entrada in enumerate(entradas_validas):
            ultimo = i == len(entradas_validas) - 1
            conector = '└── ' if ultimo else '├── '
            if entrada.is_dir():
                total_dirs += 1
                linhas_arvore.append(f'{prefixo}{conector}{entrada.name}')
                novo_prefixo = prefixo + ('    ' if ultimo else '│   ')
                _percorrer(entrada, novo_prefixo)
            else:
                total_files += 1
                linhas_arvore.append(f'{prefixo}{conector}{entrada.name}')
    _percorrer(diretorio_raiz)
    linhas_arvore.append(f'\n{total_dirs} directories, {total_files} files')
    return '\n'.join(linhas_arvore)

def juntar_scripts_python():
    diretorio_atual = Path(__file__).parent.resolve()
    arquivo_saida = diretorio_atual / 'documento_final_scripts.txt'
    script_atual = Path(__file__).resolve()
    print(f'Varrendo pasta raiz: {diretorio_atual}')
    arvore_texto = gerar_arvore_diretorio(diretorio_atual)
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
    arquivos_py = []
    for p in diretorio_atual.rglob('*.py'):
        if any((pasta in p.parts for pasta in pastas_ignoradas)):
            continue
        if p.is_file() and p.resolve() != script_atual and (p.resolve() != arquivo_saida):
            arquivos_py.append(p)
    arquivos_py = sorted(arquivos_py)
    if not arquivos_py:
        print('\n[AVISO] Nenhum ficheiro .py relevante foi encontrado nas pastas!')
        return
    print(f'Encontrados {len(arquivos_py)} ficheiros Python válidos. A escrever...')
    with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
        f_out.write(f"{'#' * 70}\n")
        f_out.write(f'# ESTRUTURA DO DIRETÓRIO (PROJECT TREE)\n')
        f_out.write(f"{'#' * 70}\n\n")
        f_out.write(arvore_texto)
        f_out.write('\n\n' + '=' * 70 + '\n\n')
        for arquivo_path in arquivos_py:
            caminho_relativo = arquivo_path.relative_to(diretorio_atual)
            print(f'-> A adicionar: {caminho_relativo}')
            f_out.write(f"{'#' * 70}\n")
            f_out.write(f'# SCRIPT: {caminho_relativo}\n')
            f_out.write(f"{'#' * 70}\n\n")
            try:
                with open(arquivo_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                    conteudo = f_in.read()
                    f_out.write(conteudo)
                    if not conteudo.endswith('\n'):
                        f_out.write('\n')
            except Exception as e:
                f_out.write(f'# [ERRO AO LER ESTE FICHEIRO: {e}]\n')
            f_out.write('\n\n')
    print(f'\nPronto! A árvore e todos os códigos foram salvos em: {arquivo_saida}')
if __name__ == '__main__':
    juntar_scripts_python()
