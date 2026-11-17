from pathlib import Path

def juntar_scripts_python():
    diretorio_atual = Path(__file__).parent.resolve()
    arquivo_saida = diretorio_atual / 'documento_final_scripts.txt'
    script_atual = Path(__file__).resolve()
    print(f'Varrendo pasta raiz: {diretorio_atual}')
    arquivos_py = []
    for p in diretorio_atual.rglob('*.py'):
        if p.is_file() and p.resolve() != script_atual and (p.resolve() != arquivo_saida):
            arquivos_py.append(p)
    if not arquivos_py:
        print('\n[AVISO] Nenhum arquivo .py foi encontrado nas pastas!')
        return
    print(f'Encontrados {len(arquivos_py)} arquivos Python. Escrevendo...')
    with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
        for arquivo_path in arquivos_py:
            caminho_relativo = arquivo_path.relative_to(diretorio_atual)
            print(f'-> Adicionando: {caminho_relativo}')
            f_out.write(f"\n{'#' * 70}\n")
            f_out.write(f'# SCRIPT: {caminho_relativo}\n')
            f_out.write(f"{'#' * 70}\n\n")
            try:
                with open(arquivo_path, 'r', encoding='utf-8') as f_in:
                    conteudo = f_in.read()
                    f_out.write(conteudo)
                    if not conteudo.endswith('\n'):
                        f_out.write('\n')
            except Exception as e:
                f_out.write(f'# [ERRO AO LER ESTE ARQUIVO: {e}]\n')
            f_out.write('\n\n')
    print(f'\nPronto! Todos os códigos foram salvos em: {arquivo_saida}')
if __name__ == '__main__':
    juntar_scripts_python()
