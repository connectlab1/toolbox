import os
import sys
import datetime
import re

def slugify(texto):
    texto = texto.lower()
    texto = re.sub('[àáâãäå]', 'a', texto)
    texto = re.sub('[èéêë]', 'e', texto)
    texto = re.sub('[ìíîï]', 'i', texto)
    texto = re.sub('[òóôõö]', 'o', texto)
    texto = re.sub('[ùúûü]', 'u', texto)
    texto = re.sub('[ç]', 'c', texto)
    texto = re.sub('[^a-z0-9\\s-]', '', texto)
    texto = re.sub('[\\s-]+', '-', texto).strip('-')
    return texto

def processar_conversao(caminho_arquivo, categoria='artigos'):
    if not os.path.exists(caminho_arquivo):
        print(f"[Erro] O arquivo '{caminho_arquivo}' não foi encontrado.")
        sys.exit(1)
    titulo_post = 'Meu Artigo'
    markdown_linhas = []
    primeiro_titulo_encontrado = False
    extensao = os.path.splitext(caminho_arquivo)[1].lower()
    if extensao == '.docx':
        try:
            import docx
        except ImportError:
            print("[Erro] A biblioteca 'python-docx' não está instalada.")
            print('Instale executando: pip install python-docx')
            sys.exit(1)
        doc = docx.Document(caminho_arquivo)
        for para in doc.paragraphs:
            texto = para.text.strip()
            if not texto:
                continue
            estilo = para.style.name.lower() if para.style and para.style.name else ''
            is_h1 = 'heading 1' in estilo or 'título 1' in estilo
            is_h2 = 'heading 2' in estilo or 'título 2' in estilo
            is_h3 = 'heading 3' in estilo or 'título 3' in estilo
            if not primeiro_titulo_encontrado and (is_h1 or len(markdown_linhas) == 0):
                titulo_post = texto
                primeiro_titulo_encontrado = True
                continue
            if is_h1:
                markdown_linhas.append(f'\n# {texto}\n')
            elif is_h2:
                markdown_linhas.append(f'\n## {texto}\n')
            elif is_h3:
                markdown_linhas.append(f'\n### {texto}\n')
            elif texto.endswith(':') and len(texto.split()) < 8 and (not any((c in texto for c in ['.', '!', '?']))):
                markdown_linhas.append(f'\n## {texto}\n')
            elif ':' in texto and (not texto.startswith('http')) and (len(texto.split(':', 1)[0]) < 35):
                parte_1, parte_2 = texto.split(':', 1)
                markdown_linhas.append(f'* **{parte_1.strip()}:**{parte_2}\n')
            else:
                markdown_linhas.append(f'{texto}\n')
    elif extensao in ['.txt', '.md']:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                texto = linha.strip()
                if not texto:
                    continue
                if texto.startswith('# ') and (not primeiro_titulo_encontrado):
                    titulo_post = texto.replace('# ', '').strip()
                    primeiro_titulo_encontrado = True
                    continue
                markdown_linhas.append(f'{texto}\n')
    else:
        print(f"[Erro] Formato '{extensao}' não suportado. Use .docx, .txt ou .md")
        sys.exit(1)
    pasta_posts = '_posts'
    os.makedirs(pasta_posts, exist_ok=True)
    data_atual = datetime.date.today().strftime('%Y-%m-%d')
    slug = slugify(titulo_post)
    nome_arquivo = f'{data_atual}-{slug}.md'
    caminho_completo = os.path.join(pasta_posts, nome_arquivo)
    conteudo_jekyll = f'---\nlayout: post\ntitle: "{titulo_post}"\ndate: {data_atual} 12:00:00 -0300\ncategories: {categoria}\n---\n\n' + '\n'.join(markdown_linhas)
    with open(caminho_completo, 'w', encoding='utf-8') as f:
        f.write(conteudo_jekyll)
    print(f'[Sucesso] Conversão total concluída!\nSalvo em: {caminho_completo}')
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python3 doc-to-md.py <arquivo.docx> [categoria]')
        sys.exit(1)
    arquivo = sys.argv[1]
    cat = sys.argv[2] if len(sys.argv) > 2 else 'artigos'
    processar_conversao(arquivo, cat)
