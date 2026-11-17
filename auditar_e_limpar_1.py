import os
import ast
import sys
import re

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

def auditar_projeto(diretorio_raiz):
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
    arquivos_py = []
    for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
        subpastas[:] = [p for p in subpastas if p not in pastas_ignoradas]
        for arquivo in arquivos:
            if arquivo.endswith('.py') and arquivo != 'auditar_e_limpar.py':
                caminho_completo = os.path.join(pasta_atual, arquivo)
                arquivos_py.append(caminho_completo)
    return arquivos_py

def main():
    diretorio_alvo = '.'
    arquivo_relatorio = 'relatorio_auditoria.txt'
    print('\n[1/3] Varrendo diretório em busca de scripts Python...')
    arquivos_py = auditar_projeto(diretorio_alvo)
    if not arquivos_py:
        print('[AVISO] Nenhum script Python encontrado neste diretório.')
        return
    print(f'[INFO] Foram encontrados {len(arquivos_py)} scripts Python.')
    print(f"[2/3] Gerando relatório consolidado em '{arquivo_relatorio}'...")
    with open(arquivo_relatorio, 'w', encoding='utf-8') as f_out:
        for caminho in arquivos_py:
            f_out.write(f"\n\n{'=' * 80}\n")
            f_out.write(f'ARQUIVO: {caminho}\n')
            f_out.write(f"{'=' * 80}\n\n")
            try:
                with open(caminho, 'r', encoding='utf-8') as f_in:
                    f_out.write(f_in.read())
                f_out.write('\n')
            except Exception as e:
                f_out.write(f'[ERRO AO LER ARQUIVO]: {e}\n')
    print(f'[SUCESSO] Relatório de auditoria gerado com sucesso!')
    print('=' * 80)
    print(f"Abra o arquivo '{arquivo_relatorio}' para inspecionar o código de todos os scripts.")
    print('=' * 80)
    print('\n[3/3] PRÓXIMA ETAPA')
    resposta = input('Deseja prosseguir para a limpeza profunda (remover comentários e docstrings de todos os scripts)? (s/n): ').strip().lower()
    if resposta == 's':
        print('\n[INFO] Aplicando limpeza de código nos arquivos originais...')
        for caminho in arquivos_py:
            try:
                with open(caminho, 'r', encoding='utf-8') as f_in:
                    conteudo_original = f_in.read()
                conteudo_limpo = limpar_codigo_string(conteudo_original)
                with open(caminho, 'w', encoding='utf-8') as f_out:
                    f_out.write(conteudo_limpo.strip() + '\n')
                print(f'  [LIMPO] {caminho}')
            except Exception as e:
                print(f'  [ERRO] Falha ao processar {caminho}: {e}')
        print('\n[SUCESSO] Auditoria e limpeza concluídas! Os scripts estão totalmente limpos e prontos.')
    else:
        print('\n[INFO] Operação de limpeza ignorada. O relatório de auditoria permanece intacto.')
if __name__ == '__main__':
    main()
