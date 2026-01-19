================================================================================
  MINUTA GENERATOR - COMO INSTALAR NO WINDOWS
  Caminho: C:\Projetos códigos\Gerador de templates
================================================================================

RESUMO RÁPIDO
==============

1. Baixe o projeto (ZIP ou TAR.GZ)
2. Extraia em: C:\Projetos códigos\Gerador de templates
3. Execute: install_windows.bat (ou install_windows.ps1)
4. Configure sua GOOGLE_API_KEY no arquivo .env
5. Use: minuta-generator generate documento.pdf -o template.html

================================================================================

PASSO A PASSO DETALHADO
========================

PASSO 1: BAIXAR O PROJETO
--------------------------

Opção A - Arquivo Compactado:
  • Baixe: minuta-generator.zip (37KB)
  • Localização: /home/user/browser-use/minuta-generator.zip

Opção B - Clonar do Git:
  git clone [URL] "C:\Projetos códigos\Gerador de templates"


PASSO 2: CRIAR DIRETÓRIO NO WINDOWS
------------------------------------

Abra o PowerShell ou Prompt de Comando:

  mkdir "C:\Projetos códigos\Gerador de templates"
  cd "C:\Projetos códigos\Gerador de templates"


PASSO 3: EXTRAIR ARQUIVOS
--------------------------

ZIP:
  • Botão direito > Extrair Aqui
  • Ou use 7-Zip / WinRAR

TAR.GZ:
  • Use 7-Zip: https://www.7-zip.org/
  • Extrair duas vezes (primeiro .gz, depois .tar)

Estrutura esperada após extração:

  C:\Projetos códigos\Gerador de templates\
  ├── minuta_generator\
  │   ├── __init__.py
  │   ├── models.py
  │   ├── cli.py
  │   └── ...
  ├── install_windows.bat
  ├── install_windows.ps1
  ├── README.md
  ├── README_WINDOWS.md
  └── pyproject.toml


PASSO 4: INSTALAR PRÉ-REQUISITOS
---------------------------------

Python 3.11 ou Superior:
  • Baixe: https://www.python.org/downloads/
  • IMPORTANTE: Marcar ✓ "Add Python to PATH" durante instalação
  • Teste: python --version


PASSO 5: EXECUTAR INSTALAÇÃO AUTOMÁTICA
----------------------------------------

Método A - Prompt de Comando (CMD):
  cd "C:\Projetos códigos\Gerador de templates"
  install_windows.bat

Método B - PowerShell (Recomendado):
  cd "C:\Projetos códigos\Gerador de templates"
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\install_windows.ps1

O script irá:
  ✓ Verificar Python
  ✓ Instalar UV (gerenciador de pacotes)
  ✓ Criar ambiente virtual (.venv)
  ✓ Instalar todas as dependências
  ✓ Criar arquivo .env


PASSO 6: CONFIGURAR API KEY
----------------------------

1. Obter chave gratuita:
   https://makersuite.google.com/app/apikey

2. Editar .env:
   notepad .env

3. Adicionar:
   GOOGLE_API_KEY=sua-chave-aqui-SEM-ASPAS

4. Salvar e fechar


PASSO 7: TESTAR INSTALAÇÃO
---------------------------

  cd "C:\Projetos códigos\Gerador de templates"
  .venv\Scripts\activate.bat
  minuta-generator --help

Se mostrar a ajuda, está funcionando! ✓


PASSO 8: PRIMEIRO USO
---------------------

Exemplo com um documento:
  minuta-generator generate "C:\Documentos\petição.pdf" -o template.html

Exemplo com múltiplos documentos:
  minuta-generator generate doc1.pdf doc2.pdf doc3.docx -o template.html

Gerar em DOCX:
  minuta-generator generate documento.pdf -o template.docx --format docx

Usar modelo local (sem API key):
  minuta-generator generate documento.pdf -o template.html --provider local

================================================================================

SOLUÇÃO DE PROBLEMAS
=====================

"python não é reconhecido":
  → Reinstale Python marcando "Add Python to PATH"
  → Ou adicione manualmente às Variáveis de Ambiente

"Acesso negado":
  → Execute CMD ou PowerShell como Administrador
  → Botão direito > "Executar como administrador"

"Scripts desabilitados" (PowerShell):
  → Execute: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  → Depois execute install_windows.ps1 novamente

"Caminho não encontrado":
  → Use aspas duplas em caminhos com espaços
  → cd "C:\Projetos códigos\Gerador de templates"

Dependências não instalam:
  → python -m pip install --upgrade pip
  → uv pip install -e . --force-reinstall

================================================================================

ARQUIVOS DE AJUDA
=================

Dentro do projeto, consulte:

  • README_WINDOWS.md          - Guia completo para Windows
  • INSTRUCOES_INSTALACAO_WINDOWS.md  - Instruções detalhadas
  • README.md                  - Documentação principal
  • QUICKSTART.md              - Início rápido
  • example_usage.py           - Exemplos de código Python

================================================================================

CRIAR ATALHO NA ÁREA DE TRABALHO
=================================

1. Crie arquivo: Minuta Generator.bat na área de trabalho
2. Edite e adicione:

@echo off
cd /d "C:\Projetos códigos\Gerador de templates"
call .venv\Scripts\activate.bat
echo Minuta Generator - Pronto!
cmd /k

3. Salve e clique duas vezes para usar

================================================================================

ESTRUTURA RECOMENDADA
======================

C:\Projetos códigos\
│
├── Gerador de templates\        ← Projeto aqui
│   ├── minuta_generator\
│   ├── .venv\
│   └── ...
│
├── Documentos\                  ← Documentos originais
│   ├── Petições\
│   ├── Contestações\
│   └── Recursos\
│
└── Templates Gerados\           ← Saída do programa
    ├── template_petição.html
    └── ...

================================================================================

ARQUIVOS DISPONÍVEIS PARA DOWNLOAD
===================================

  • minuta-generator.zip      (37 KB) - Recomendado para Windows
  • minuta-generator.tar.gz   (24 KB) - Para Linux/Mac

Localização no servidor Linux:
  /home/user/browser-use/minuta-generator.zip
  /home/user/browser-use/minuta-generator.tar.gz

================================================================================

SUPORTE
=======

Problemas? Consulte:
  1. README_WINDOWS.md (no projeto)
  2. INSTRUCOES_INSTALACAO_WINDOWS.md (raiz do repositório)
  3. Entre em contato com a equipe de desenvolvimento

================================================================================

CHECKLIST DE INSTALAÇÃO
========================

□ Python 3.11+ instalado e no PATH
□ Diretório criado: C:\Projetos códigos\Gerador de templates
□ Arquivos extraídos corretamente
□ install_windows.bat ou .ps1 executado com sucesso
□ Arquivo .env criado com GOOGLE_API_KEY
□ Comando "minuta-generator --help" funciona
□ Primeiro teste realizado

================================================================================

Desenvolvido pela equipe de Legal Tech da PGM
================================================================================
