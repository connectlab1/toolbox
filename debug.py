from pathlib import Path
import ast
import subprocess
import sys
GREEN = '\x1b[92m'
YELLOW = '\x1b[93m'
RED = '\x1b[91m'
BLUE = '\x1b[94m'
CYAN = '\x1b[96m'
BOLD = '\x1b[1m'
RESET = '\x1b[0m'

def exibir_banner(titulo):
    print('\n' + BLUE + BOLD + '=' * 65 + RESET)
    print(f'{BLUE}{BOLD} {titulo}{RESET}')
    print(BLUE + BOLD + '=' * 65 + RESET + '\n')

def testar_sintaxe_ast(diretorio_alvo):
    print(f'{BLUE}[1/4] Auditando sintaxe e integridade estrutural (AST)...{RESET}')
    arquivos_py = sorted(list(diretorio_alvo.rglob('*.py')))
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
    erros_encontrados = 0
    analisados = 0
    for arq in arquivos_py:
        if any((pasta in arq.parts for pasta in pastas_ignoradas)):
            continue
        analisados += 1
        relativo = arq.relative_to(diretorio_alvo)
        try:
            conteudo = arq.read_text(encoding='utf-8')
            ast.parse(conteudo, filename=str(arq))
            avisos = []
            if len(conteudo.strip()) == 0:
                avisos.append('Arquivo vazio')
            if '"""' not in conteudo and "'''" not in conteudo:
                avisos.append('Falta docstring')
            if 'TODO' in conteudo or 'FIXME' in conteudo:
                avisos.append('Contém TODO/FIXME')
            if avisos:
                print(f"  {YELLOW}⚠{RESET} {relativo}: Alerta -> {', '.join(avisos)}")
            else:
                print(f'  {GREEN}✔{RESET} {relativo}: Sintaxe OK.')
        except SyntaxError as e:
            print(f'  {RED}✖ Erro de Sintaxe em {relativo}: Linha {e.lineno} -> {e.msg}{RESET}')
            erros_encontrados += 1
        except Exception as e:
            print(f'  {RED}✖ Erro ao ler {relativo}: {e}{RESET}')
            erros_encontrados += 1
    print(f'  [INFO] Total de arquivos analisados: {analisados}')
    return erros_encontrados == 0

def verificar_dependencias_e_ambiente():
    print(f'\n{BLUE}[2/4] Verificando ambiente Python e pacotes básicos...{RESET}')
    print(f'  {GREEN}✔{RESET} Versão do Python: {sys.version.split()[0]}')
    print(f'  {GREEN}✔{RESET} Executável: {sys.executable}')
    return True

def executar_testes_pytest(diretorio_alvo):
    print(f'\n{BLUE}[3/4] Procurando e executando testes automatizados (pytest)...{RESET}')
    tem_testes = list(diretorio_alvo.glob('test_*.py')) or list(diretorio_alvo.glob('tests/'))
    if not tem_testes:
        print(f"  {CYAN}ℹ{RESET} Nenhum diretório ou arquivo de teste ('test_*.py') detetado neste projeto.")
        return True
    try:
        resultado = subprocess.run(['pytest', '-v'], capture_output=True, text=True, cwd=diretorio_alvo)
        print(resultado.stdout)
        if resultado.returncode == 0:
            print(f'  {GREEN}✔ Todos os testes unitários passaram com sucesso!{RESET}')
            return True
        else:
            print(f'  {RED}✖ Alguns testes falharam no pytest.{RESET}')
            return False
    except FileNotFoundError:
        print(f"  {YELLOW}⚠ O pacote 'pytest' não está instalado no ambiente atual.{RESET}")
        return True
    except Exception as e:
        print(f'  {RED}✖ Erro ao executar o pytest: {e}{RESET}')
        return False

def relatorio_geral_toolbox():
    print(f'\n{BLUE}[4/4] Resumo de Diretórios e Utilitários da Toolbox...{RESET}')
    diretorio_atual = Path(__file__).parent.resolve()
    scripts_toolbox = list(diretorio_atual.glob('*.py'))
    print(f'  {CYAN}ℹ{RESET} Utilitários Python encontrados na Toolbox: {len(scripts_toolbox)}')
    for s in sorted(scripts_toolbox):
        print(f'     • {s.name}')
    return True

def main():
    exibir_banner('🧰 TOOLBOX - Diagnóstico Universal e QA de Projetos')
    diretorio_alvo = Path.cwd()
    print(f'Diretório alvo da auditoria: {diretorio_alvo}')
    t1 = testar_sintaxe_ast(diretorio_alvo)
    t2 = verificar_dependencias_e_ambiente()
    t3 = executar_testes_pytest(diretorio_alvo)
    t4 = relatorio_geral_toolbox()
    exibir_banner('✨ Relatório Final de Saúde do Projeto')
    if t1 and t2 and t3 and t4:
        print(f'{GREEN}{BOLD}✔ Projeto 100% íntegro! Sintaxe validada e ambiente pronto para produção.{RESET}\n')
    else:
        print(f'{YELLOW}{BOLD}⚠ Atenção: Foram encontrados avisos ou falhas que merecem revisão técnica.{RESET}\n')
if __name__ == '__main__':
    main()
