from pathlib import Path
import ast
import re
import sys

class RemoveDocstrings(ast.NodeTransformer):

    def _remover_docstring(self, node):
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body.pop(0)
        return node

    def visit_Module(self, node):
        self._remover_docstring(node)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self._remover_docstring(node)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._remover_docstring(node)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        self._remover_docstring(node)
        return self.generic_visit(node)

def limpar_codigo_string(codigo_fonte):
    try:
        arvore = ast.parse(codigo_fonte)
        transformador = RemoveDocstrings()
        arvore_limpa = transformador.visit(arvore)
        codigo_limpo = ast.unparse(arvore_limpa)
        return re.sub('\\n{3,}', '\n\n', codigo_limpo)
    except Exception:
        return codigo_fonte

def gerar_arvore_diretorio(diretorio_raiz, arquivos_ignorados_raiz):
    diretorio_raiz = Path(diretorio_raiz).resolve()
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
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
            if pasta_atual == diretorio_raiz and e.name in arquivos_ignorados_raiz:
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

def auditar_projeto(diretorio_raiz):
    diretorio_raiz = Path(diretorio_raiz).resolve()
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
    script_atual = Path(__file__).resolve()
    arquivos_py = []
    for p in diretorio_raiz.rglob('*.py'):
        if any((pasta in p.parts for pasta in pastas_ignoradas)):
            continue
        if p.resolve() == script_atual:
            continue
        if p.is_file():
            arquivos_py.append(p)
    return sorted(arquivos_py)

def gerar_relatorio_consolidado(diretorio_alvo, arquivos_py, caminho_saida, titulo_etapa, arquivos_ignorados_arvore):
    arvore_texto = gerar_arvore_diretorio(diretorio_alvo, arquivos_ignorados_arvore)
    with open(caminho_saida, 'w', encoding='utf-8') as f_out:
        f_out.write(f"{'#' * 70}\n")
        f_out.write(f'# RELATÓRIO DE AUDITORIA ({titulo_etapa})\n')
        f_out.write(f'# ESTRUTURA DO DIRETÓRIO (PROJECT TREE)\n')
        f_out.write(f"{'#' * 70}\n\n")
        f_out.write(arvore_texto)
        f_out.write('\n\n' + '=' * 80 + '\n\n')
        for caminho in arquivos_py:
            caminho_relativo = caminho.relative_to(diretorio_alvo)
            f_out.write(f"{'=' * 80}\n")
            f_out.write(f'ARQUIVO: {caminho_relativo}\n')
            f_out.write(f"{'=' * 80}\n\n")
            try:
                with open(caminho, 'r', encoding='utf-8', errors='ignore') as f_in:
                    f_out.write(f_in.read())
                f_out.write('\n\n')
            except Exception as e:
                f_out.write(f'[ERRO AO LER FICHEIRO]: {e}\n\n')

def main():
    diretorio_alvo = Path(__file__).parent.resolve()
    relatorio_antes = diretorio_alvo / 'relatorio_auditoria_antes.txt'
    relatorio_depois = diretorio_alvo / 'relatorio_auditoria_depois.txt'
    relatorios_nomes = {relatorio_antes.name, relatorio_depois.name}
    print('\n[1/4] A varrer o diretório em busca de scripts Python...')
    arquivos_py = auditar_projeto(diretorio_alvo)
    if not arquivos_py:
        print('[AVISO] Nenhum script Python encontrado neste diretório.')
        return
    print(f'[INFO] Foram encontrados {len(arquivos_py)} scripts Python válidos.')
    print(f"[2/4] A gerar relatório inicial (ANTES) em '{relatorio_antes.name}'...")
    gerar_relatorio_consolidado(diretorio_alvo=diretorio_alvo, arquivos_py=arquivos_py, caminho_saida=relatorio_antes, titulo_etapa='ANTES DA LIMPEZA', arquivos_ignorados_arvore=relatorios_nomes)
    print(f"[SUCESSO] Snapshot original salvo em '{relatorio_antes.name}'!")
    print('=' * 80)
    print('\n[3/4] ETAPA DE LIMPEZA')
    resposta = input('Deseja prosseguir para a limpeza profunda (remover comentários e docstrings de todos os scripts)? (s/n): ').strip().lower()
    if resposta == 's':
        print('\n[INFO] A aplicar limpeza de código nos ficheiros originais...')
        for caminho in arquivos_py:
            caminho_relativo = caminho.relative_to(diretorio_alvo)
            try:
                with open(caminho, 'r', encoding='utf-8', errors='ignore') as f_in:
                    conteudo_original = f_in.read()
                conteudo_limpo = limpar_codigo_string(conteudo_original)
                with open(caminho, 'w', encoding='utf-8') as f_out:
                    f_out.write(conteudo_limpo.strip() + '\n')
                print(f'  [LIMPO] {caminho_relativo}')
            except Exception as e:
                print(f'  [ERRO] Falha ao processar {caminho_relativo}: {e}')
        print(f"\n[4/4] A gerar relatório final (DEPOIS) em '{relatorio_depois.name}'...")
        gerar_relatorio_consolidado(diretorio_alvo=diretorio_alvo, arquivos_py=arquivos_py, caminho_saida=relatorio_depois, titulo_etapa='DEPOIS DA LIMPEZA', arquivos_ignorados_arvore=relatorios_nomes)
        print(f'\n[SUCESSO] Auditoria completa!')
        print(f'  -> Código original preservado em: {relatorio_antes.name}')
        print(f'  -> Código limpo consolidado em: {relatorio_depois.name}')
    else:
        print(f"\n[INFO] Operação de limpeza ignorada. Apenas '{relatorio_antes.name}' foi gerado e os arquivos originais permanecem intactos.")
if __name__ == '__main__':
    main()
