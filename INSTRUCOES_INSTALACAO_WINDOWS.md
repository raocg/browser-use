# 🚀 Instruções de Instalação - Gerador de Templates de Minutas

## 📦 Como Instalar no Windows

### Caminho de Instalação Desejado:
```
C:\Projetos códigos\Gerador de templates
```

---

## Método 1: Usando Arquivo Compactado (Recomendado)

### Passo 1: Baixar o Projeto

Você tem duas opções:

**Opção A: Arquivo no repositório**
- Baixe o arquivo `minuta-generator.tar.gz` ou `minuta-generator.zip`

**Opção B: Clonar do Git**
```cmd
git clone [URL-DO-REPOSITORIO] "C:\Projetos códigos\Gerador de templates"
```

### Passo 2: Criar o Diretório

Abra o **PowerShell** ou **Prompt de Comando**:

```cmd
mkdir "C:\Projetos códigos\Gerador de templates"
cd "C:\Projetos códigos\Gerador de templates"
```

### Passo 3: Extrair os Arquivos

#### Se baixou .zip:
1. Clique com botão direito no arquivo
2. Escolha "Extrair Aqui" ou "Extrair Tudo"
3. Mova os arquivos extraídos para `C:\Projetos códigos\Gerador de templates`

#### Se baixou .tar.gz:
1. Use 7-Zip (https://www.7-zip.org/) ou WinRAR
2. Extrair > "Extrair Aqui"
3. Mover para o diretório desejado

### Passo 4: Instalar Pré-requisitos

#### Python 3.11+

1. Baixe: https://www.python.org/downloads/
2. **IMPORTANTE**: Durante a instalação, marque ✅ "Add Python to PATH"
3. Teste no terminal:
   ```cmd
   python --version
   ```

### Passo 5: Executar Instalação Automática

No diretório do projeto:

#### Usando Batch (Prompt de Comando):
```cmd
cd "C:\Projetos códigos\Gerador de templates"
install_windows.bat
```

#### Usando PowerShell (Recomendado):
```powershell
cd "C:\Projetos códigos\Gerador de templates"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install_windows.ps1
```

### Passo 6: Configurar API Key

1. Obtenha uma chave gratuita: https://makersuite.google.com/app/apikey

2. Edite o arquivo `.env`:
   ```cmd
   notepad .env
   ```

3. Adicione:
   ```env
   GOOGLE_API_KEY=sua-chave-aqui-123456789
   ```

4. Salve e feche

### Passo 7: Testar

```cmd
cd "C:\Projetos códigos\Gerador de templates"
.venv\Scripts\activate.bat
minuta-generator --help
```

Se mostrar a ajuda, está funcionando! ✅

---

## Método 2: Instalação Manual (Se Automática Falhar)

### 1. Criar Diretório
```cmd
mkdir "C:\Projetos códigos\Gerador de templates"
cd "C:\Projetos códigos\Gerador de templates"
```

### 2. Extrair Todos os Arquivos

Certifique-se de que a estrutura fique assim:
```
C:\Projetos códigos\Gerador de templates\
├── minuta_generator\
│   ├── __init__.py
│   ├── models.py
│   ├── cli.py
│   └── ...
├── pyproject.toml
├── README.md
└── install_windows.bat
```

### 3. Instalar UV
```cmd
python -m pip install uv
```

### 4. Criar Ambiente Virtual
```cmd
python -m venv .venv
```

### 5. Ativar Ambiente
```cmd
.venv\Scripts\activate.bat
```

### 6. Instalar Dependências
```cmd
pip install -e .
```

Ou:
```cmd
uv pip install -e .
```

### 7. Configurar .env
```cmd
copy .env.example .env
notepad .env
```

Adicione sua `GOOGLE_API_KEY`

### 8. Testar
```cmd
minuta-generator --help
```

---

## 🎯 Primeiro Uso

### Exemplo Básico

Crie uma pasta de teste:
```cmd
mkdir "C:\Projetos códigos\Documentos Teste"
```

Copie um PDF de petição para lá e execute:

```cmd
cd "C:\Projetos códigos\Gerador de templates"
.venv\Scripts\activate.bat

minuta-generator generate "C:\Projetos códigos\Documentos Teste\petição.pdf" -o template.html
```

Abra `template.html` no navegador para ver o resultado!

---

## 🛠️ Solução de Problemas Comuns

### "python não é reconhecido"

**Problema**: Python não está no PATH

**Solução**:
1. Pesquise "Variáveis de Ambiente" no Windows
2. Em "Variáveis do Sistema", encontre "Path"
3. Adicione: `C:\Python311` (ou onde instalou Python)
4. Adicione: `C:\Python311\Scripts`
5. Reinicie o terminal

### "Acesso negado" ao instalar

**Problema**: Falta de permissões

**Solução**:
- Execute o Prompt de Comando ou PowerShell como **Administrador**
- Clique com botão direito > "Executar como administrador"

### "Scripts desabilitados" (PowerShell)

**Problema**: Política de execução do PowerShell

**Solução**:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois execute o script novamente.

### "Não foi possível encontrar o caminho"

**Problema**: Caminho com espaços

**Solução**: Sempre use aspas duplas:
```cmd
cd "C:\Projetos códigos\Gerador de templates"
```

### Dependências não instalam

**Problema**: Problemas de rede ou cache

**Solução**:
```cmd
python -m pip install --upgrade pip
python -m pip cache purge
uv pip install -e . --force-reinstall
```

---

## 📁 Estrutura Recomendada de Pastas

Organize assim:

```
C:\Projetos códigos\
│
├── Gerador de templates\          ← Projeto instalado
│   ├── minuta_generator\
│   ├── .venv\
│   ├── README.md
│   └── ...
│
├── Documentos\                     ← Seus documentos originais
│   ├── Petições\
│   │   ├── petição1.pdf
│   │   ├── petição2.pdf
│   │   └── petição3.pdf
│   ├── Contestações\
│   └── Recursos\
│
└── Templates Gerados\              ← Saída do programa
    ├── template_petição.html
    ├── template_contestação.docx
    └── template_recurso.html
```

---

## 🚀 Criar Atalho na Área de Trabalho

1. Crie um novo arquivo de texto na área de trabalho
2. Renomeie para `Minuta Generator.bat`
3. Edite com o Notepad e adicione:

```batch
@echo off
cd /d "C:\Projetos códigos\Gerador de templates"
call .venv\Scripts\activate.bat
echo ========================================
echo   Minuta Generator - Pronto para Usar!
echo ========================================
echo.
echo Digite: minuta-generator --help
echo.
cmd /k
```

4. Salve e feche
5. Clique duas vezes para abrir terminal pronto!

---

## 📞 Suporte Adicional

Consulte os seguintes arquivos no projeto:

- **README_WINDOWS.md** - Guia completo para Windows
- **README.md** - Documentação principal
- **QUICKSTART.md** - Início rápido
- **example_usage.py** - Exemplos de código

---

## ✅ Checklist de Instalação

- [ ] Python 3.11+ instalado
- [ ] Python adicionado ao PATH
- [ ] Diretório criado: `C:\Projetos códigos\Gerador de templates`
- [ ] Arquivos extraídos no diretório correto
- [ ] Script de instalação executado (`install_windows.bat` ou `install_windows.ps1`)
- [ ] Arquivo `.env` criado e configurado com GOOGLE_API_KEY
- [ ] Comando `minuta-generator --help` funciona
- [ ] Primeiro teste realizado com sucesso

---

**Pronto!** Você está preparado para usar o Gerador de Templates de Minutas Jurídicas! 🎉

Para dúvidas específicas, consulte o README_WINDOWS.md ou entre em contato com a equipe de desenvolvimento.
