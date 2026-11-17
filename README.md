# Toolbox 🧰

Uma coleção de utilitários em Python desenvolvidos para automatizar tarefas diárias de desenvolvimento, manutenção de ambientes, auditoria de código, união de scripts e conversão de formatos. 

Este repositório centraliza ferramentas leves, modulares e independentes que funcionam de forma multiplataforma (Linux, Windows e macOS) utilizando bibliotecas nativas do Python.

---

## 🛠️ Ferramentas Disponíveis

### 1. `unir_scripts2.py` (Consolidador de Projetos com Árvore)
* **O que faz:** Varre recursivamente o diretório do projeto à procura de ficheiros `.py`, gera um mapa visual da estrutura de pastas em formato de árvore (*Project Tree*) e consolida o código de todos os scripts num único documento de texto (`documento_final_scripts.txt`).
* **Destaques:** Ordenação alfabética estrita, exclusão automática de pastas de sistema/cache (`.git`, `venv`, `__pycache__`, etc.) e autoexclusão para evitar loops.

### 2. `auditar_e_limpar_2.py` (Auditoria e Limpeza Profunda via AST)
* **O que faz:** Uma ferramenta de auditoria totalmente autónoma. Gera primeiro um snapshot completo do estado original (`relatorio_auditoria_antes.txt`) contendo a árvore de diretórios e o código intacto. Após confirmação interativa do utilizador, aplica uma limpeza profunda baseada em AST (removendo comentários e *docstrings*) e gera um relatório final (`relatorio_auditoria_depois.txt`).
* **Destaques:** Blindagem absoluta contra autoescrevimento acidental (mesmo que mude de nome) e preservação total do código original antes de qualquer alteração destrutiva.

### 3. `buscar_palavra.py` (Pesquisa Textual Recursiva / Grep)
* **O que faz:** Permite procurar por uma palavra ou termo específico em todos os ficheiros do projeto de forma recursiva, indicando o ficheiro exato e o número da linha correspondente.

### 4. `doc-to-md.py` (Conversor de Documentos para Markdown)
* **O que faz:** Transforma ficheiros de texto ou documentos do Word (`.docx`) estruturados em posts formatados em Markdown (`.md`), prontos para serem utilizados em geradores de sites estáticos ou blogs (como o Jekyll na pasta `_posts`).

### 5. `basic-math.py` / `math.py` (Geradores de Exercícios)
* **O que faz:** Utilitários simples focados na geração automatizada de operações matemáticas básicas (soma, subtração, multiplicação e divisão) com números aleatórios.

---

## 🚀 Como Utilizar

Certifique-se de que tem o **Python 3** instalado no seu sistema. Clone o repositório e execute o script desejado diretamente a partir do terminal:

```bash
# Clonar o repositório
git clone https://github.com/connectlab1/toolbox.git
cd toolbox

# Executar o consolidador de scripts
python3 unir_scripts2.py

# Executar a auditoria e limpeza segura
python3 auditar_e_limpar_2.py

# Procurar por um termo específico no código
python3 buscar_palavra.py "termo_a_procurar"
