# Minuta Generator - Guia de Instalação para Windows

## 📍 Instalação no Caminho Desejado

### Passo 1: Criar o Diretório

Abra o **PowerShell** ou **Prompt de Comando** como Administrador e execute:

```cmd
mkdir "C:\Projetos códigos\Gerador de templates"
cd "C:\Projetos códigos\Gerador de templates"
```

### Passo 2: Extrair o Projeto

Se você recebeu o arquivo compactado:

1. **Se for .tar.gz**: Use 7-Zip ou WinRAR para extrair
2. **Se for .zip**: Clique com botão direito > Extrair Aqui

Ou, se você tem acesso ao repositório Git:

```cmd
git clone [URL-DO-REPOSITORIO] .
```

Após extrair, a estrutura deve ficar:

```
C:\Projetos códigos\Gerador de templates\
├── minuta_generator\
│   ├── __init__.py
│   ├── models.py
│   ├── cli.py
│   ├── readers\
│   ├── llm\
│   ├── analyzer\
│   ├── templates\
│   └── writers\
├── README.md
├── pyproject.toml
└── install_windows.bat
```

### Passo 3: Pré-requisitos

#### Python 3.11 ou Superior

1. Baixe em: https://www.python.org/downloads/
2. Durante a instalação, **MARQUE**: ✅ "Add Python to PATH"
3. Verifique a instalação:

```cmd
python --version
```

Deve mostrar: `Python 3.11.x` ou superior

#### UV (Gerenciador de Pacotes)

Será instalado automaticamente pelo script, ou instale manualmente:

```cmd
python -m pip install uv
```

### Passo 4: Executar Instalação Automática

No diretório do projeto, execute:

```cmd
install_windows.bat
```

Este script irá:
- ✅ Verificar Python
- ✅ Instalar UV
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências

### Passo 5: Configurar API Key

#### Opção A: Google Gemini (Recomendado)

1. Obtenha uma API key em: https://makersuite.google.com/app/apikey

2. Copie o arquivo de exemplo:
   ```cmd
   copy .env.example .env
   ```

3. Edite `.env` com o Notepad:
   ```cmd
   notepad .env
   ```

4. Adicione sua chave:
   ```env
   GOOGLE_API_KEY=SuaChaveAqui123456789
   ```

#### Opção B: Modelo Local (Ollama)

1. Baixe e instale Ollama: https://ollama.ai/download

2. Abra um terminal e baixe um modelo:
   ```cmd
   ollama pull llama3.2
   ```

3. Não precisa de API key para usar modelo local!

## 🚀 Como Usar

### Ativar o Ambiente Virtual

**Sempre** que for usar o programa, ative o ambiente primeiro:

```cmd
cd "C:\Projetos códigos\Gerador de templates"
.venv\Scripts\activate.bat
```

Você verá `(.venv)` no início da linha de comando.

### Comandos Básicos

#### Gerar Template de um Documento

```cmd
minuta-generator generate "C:\Documentos\petição.pdf" -o template.html
```

#### Gerar Template de Múltiplos Documentos

```cmd
minuta-generator generate "C:\Documentos\doc1.pdf" "C:\Documentos\doc2.pdf" -o template.html
```

#### Gerar em DOCX

```cmd
minuta-generator generate documento.pdf -o template.docx --format docx
```

#### Analisar Documento (sem gerar template)

```cmd
minuta-generator analyze documento.pdf
```

#### Usar Modelo Local

```cmd
minuta-generator generate documento.pdf -o template.html --provider local
```

### Exemplos com Caminhos Windows

```cmd
REM Exemplo 1: Um único PDF
minuta-generator generate "C:\Users\Seu Nome\Documents\petição.pdf" -o "C:\Output\template.html"

REM Exemplo 2: Múltiplos arquivos
minuta-generator generate ^
    "C:\Documentos\doc1.pdf" ^
    "C:\Documentos\doc2.docx" ^
    "C:\Documentos\doc3.html" ^
    -o "C:\Output\template.html"

REM Exemplo 3: Usar coringas (wildcard)
cd "C:\Documentos\Minutas"
minuta-generator generate *.pdf -o template_consolidado.html

REM Exemplo 4: Modelo local
minuta-generator generate documento.pdf -o template.html --provider local --model llama3.2
```

## 🛠️ Solução de Problemas

### Erro: "Python não encontrado"

**Solução**:
1. Reinstale Python marcando "Add Python to PATH"
2. Ou adicione manualmente ao PATH:
   - Pesquise "Variáveis de Ambiente" no Windows
   - Adicione `C:\Python311` (ou onde instalou) ao PATH

### Erro: "uv não encontrado"

**Solução**:
```cmd
python -m pip install --upgrade pip
python -m pip install uv
```

### Erro: "Google API key é necessária"

**Solução**:
```cmd
REM Opção 1: Definir variável de ambiente temporariamente
set GOOGLE_API_KEY=SuaChaveAqui

REM Opção 2: Criar arquivo .env (recomendado)
copy .env.example .env
notepad .env
```

### Erro: "No module named 'pydantic'"

**Solução**:
```cmd
.venv\Scripts\activate.bat
uv pip install -e .
```

### Erro ao Processar Caminhos com Espaços

**Solução**: Use aspas duplas:
```cmd
REM ❌ Errado
minuta-generator generate C:\Projetos códigos\doc.pdf -o template.html

REM ✅ Correto
minuta-generator generate "C:\Projetos códigos\doc.pdf" -o template.html
```

## 📝 Criar Atalho para Fácil Acesso

1. Crie um arquivo `minuta-generator.bat` na área de trabalho:

```batch
@echo off
cd /d "C:\Projetos códigos\Gerador de templates"
call .venv\Scripts\activate.bat
cmd /k
```

2. Clique duas vezes no atalho para abrir terminal com ambiente ativado!

## 🔄 Atualizar o Projeto

Se houver atualizações:

```cmd
cd "C:\Projetos códigos\Gerador de templates"
git pull origin main
.venv\Scripts\activate.bat
uv pip install -e . --upgrade
```

## 📚 Estrutura de Diretórios Recomendada

```
C:\Projetos códigos\
├── Gerador de templates\       (projeto instalado aqui)
│   ├── minuta_generator\
│   ├── .venv\
│   └── ...
│
├── Documentos Entrada\         (seus documentos originais)
│   ├── petições\
│   ├── contestações\
│   └── recursos\
│
└── Templates Gerados\          (saída do programa)
    ├── template_petição.html
    ├── template_contestação.docx
    └── ...
```

## 💡 Dicas para Windows

### Usar PowerShell (Recomendado)

PowerShell tem melhor suporte a caracteres especiais:

```powershell
# Ativar ambiente
& "C:\Projetos códigos\Gerador de templates\.venv\Scripts\Activate.ps1"

# Usar o programa
minuta-generator generate "C:\Docs\arquivo.pdf" -o template.html
```

### Criar Alias (PowerShell)

Adicione ao seu perfil do PowerShell:

```powershell
# Abra o perfil
notepad $PROFILE

# Adicione esta linha:
function mg { & "C:\Projetos códigos\Gerador de templates\.venv\Scripts\minuta-generator.exe" $args }

# Agora pode usar:
mg generate documento.pdf -o template.html
```

## 🎯 Primeiro Teste

Depois de instalar, teste com este comando:

```cmd
cd "C:\Projetos códigos\Gerador de templates"
.venv\Scripts\activate.bat
minuta-generator --help
```

Deve mostrar a ajuda do programa. ✅

Se precisar de ajuda, consulte o README.md principal ou os exemplos em `example_usage.py`.

## 🔧 Desenvolvimento no Windows

Se você quiser modificar o código:

### Editor Recomendado: VS Code

1. Baixe: https://code.visualstudio.com/
2. Instale extensão "Python" da Microsoft
3. Abra o projeto:
   ```cmd
   code "C:\Projetos códigos\Gerador de templates"
   ```

### Executar Testes

```cmd
.venv\Scripts\activate.bat
pytest -vxs tests/
```

### Type Checking

```cmd
.venv\Scripts\activate.bat
pyright
```

### Formatação

```cmd
.venv\Scripts\activate.bat
ruff check --fix
ruff format
```

## 📞 Suporte

Para problemas específicos do Windows, verifique:
- Python instalado corretamente com "Add to PATH"
- Antivírus não está bloqueando a instalação
- Permissões de escrita no diretório
- Caminhos usando aspas duplas quando há espaços

---

**Desenvolvido pela equipe de Legal Tech da PGM**
