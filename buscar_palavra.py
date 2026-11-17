from pathlib import Path
import sys

def buscar_por_nome(termo_busca, diretorio_raiz):
    """Busca arquivos ou pastas cujo nome contenha o termo informado."""
    diretorio_raiz = Path(diretorio_raiz).resolve()
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
    termo_lower = termo_busca.lower()
    
    encontrados = 0
    script_atual = Path(__file__).resolve()

    print(f"\n[INFO] Procurando arquivos com o nome contendo '{termo_busca}' a partir de '{diretorio_raiz}'...\n")
    print('=' * 80)

    for p in diretorio_raiz.rglob('*'):
        if any(pasta in p.parts for pasta in pastas_ignoradas):
            continue
        if p.resolve() == script_atual:
            continue

        if termo_lower in p.name.lower():
            encontrados += 1
            caminho_relativo = p.relative_to(diretorio_raiz)
            tipo = "📁 Pasta" if p.is_dir() else "📄 Arquivo"
            print(f'{tipo}: {caminho_relativo}')
            print('-' * 80)

    print(f'\n[BUSCA POR NOME CONCLUÍDA]')
    print(f'Total de itens encontrados: {encontrados}')

def buscar_por_conteudo(termo_busca, diretorio_raiz):
    """Busca o termo dentro do conteúdo de arquivos de texto/código válidos."""
    diretorio_raiz = Path(diretorio_raiz).resolve()
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode'}
    
    extensoes_texto = {
        '.py', '.txt', '.md', '.json', '.html', '.css', 
        '.js', '.yml', '.yaml', '.sh', '.ini', '.cfg', '.csv'
    }
    
    termo_lower = termo_busca.lower()
    total_ocorrencias = 0
    arquivos_afetados = set()
    script_atual = Path(__file__).resolve()

    print(f"\n[INFO] Buscando pelo termo '{termo_busca}' no CONTEÚDO dos arquivos a partir de '{diretorio_raiz}'...\n")
    print('=' * 80)

    for p in diretorio_raiz.rglob('*'):
        if any(pasta in p.parts for pasta in pastas_ignoradas):
            continue
        if p.is_dir() or p.resolve() == script_atual:
            continue

        if p.suffix.lower() in extensoes_texto:
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                    for numero_linha, linha in enumerate(f, 1):
                        if termo_lower in linha.lower():
                            total_ocorrencias += 1
                            arquivos_afetados.add(str(p))
                            
                            linha_limpa = linha.strip()
                            if len(linha_limpa) > 150:
                                linha_limpa = linha_limpa[:147] + "..."
                                
                            caminho_relativo = p.relative_to(diretorio_raiz)
                            print(f'📄 Arquivo: {caminho_relativo}')
                            print(f'   └── Linha {numero_linha}: {linha_limpa}')
                            print('-' * 80)
            except Exception:
                pass

    print(f'\n[BUSCA POR CONTEÚDO CONCLUÍDA]')
    print(f'Total de ocorrências encontradas: {total_ocorrencias}')
    print(f'Total de arquivos únicos afetados: {len(arquivos_afetados)}')

def main():
    diretorio_atual = Path(__file__).parent.resolve()

    print("=" * 50)
    print(" 🧰 TOOLBOX - MENU DE BUSCA INTELIGENTE")
    print("=" * 50)
    print(" [1] Buscar por Nome de Arquivo/Pasta (ex: imagens, scripts, etc.)")
    print(" [2] Buscar por Termo/Palavra DENTRO do Conteúdo dos arquivos")
    print(" [0] Sair")
    print("-" * 50)

    opcao = input("Escolha o modo de busca desejado (0-2): ").strip()

    if opcao == '0':
        print("[INFO] Operação cancelada.")
        return
    elif opcao in ('1', '2'):
        termo = input("Digite o termo ou palavra que deseja procurar: ").strip()
        if not termo:
            print("[AVISO] Nenhum termo informado. Operação cancelada.")
            return

        if opcao == '1':
            buscar_por_nome(termo, diretorio_atual)
        elif opcao == '2':
            buscar_por_conteudo(termo, diretorio_atual)
    else:
        print("[ERRO] Opção inválida. Execute o script novamente.")

if __name__ == '__main__':
    main()
