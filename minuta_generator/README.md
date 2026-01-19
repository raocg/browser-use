# Minuta Generator

Sistema de automação para criação de templates de minutas jurídicas usando Inteligência Artificial.

## Visão Geral

O **Minuta Generator** analisa documentos jurídicos existentes (petições, contestações, recursos) e automaticamente:

1. 📄 **Lê documentos** em múltiplos formatos (PDF, DOCX, HTML)
2. 🔍 **Identifica padrões** comuns usando LLMs (Google Gemini ou modelos locais)
3. 🏗️ **Gera templates** reutilizáveis com placeholders para partes variáveis
4. 💾 **Exporta** templates em HTML ou DOCX com formatação visual

## Características

- ✅ Suporte para **múltiplos formatos** de entrada: PDF, DOC, DOCX, HTML
- ✅ **Análise com IA** usando Google Gemini ou modelos locais (Ollama)
- ✅ Identificação automática de **partes variáveis** (nomes, datas, números de processo)
- ✅ Geração de templates em **HTML** (com visualização interativa) ou **DOCX**
- ✅ Interface de linha de comando **simples e intuitiva**
- ✅ Suporte para análise de **documentos únicos ou múltiplos**

## Instalação

### Pré-requisitos

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes Python)

### Setup

```bash
# Clone ou navegue até o diretório do projeto
cd minuta_generator

# Crie o ambiente virtual e instale dependências
uv venv --python 3.11
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv pip install -e .
```

### Configuração de LLM

#### Opção 1: Google Gemini (Recomendado)

1. Obtenha uma API key em: https://makersuite.google.com/app/apikey
2. Configure a variável de ambiente:

```bash
export GOOGLE_API_KEY="sua-api-key-aqui"
```

Ou crie um arquivo `.env`:

```env
GOOGLE_API_KEY=sua-api-key-aqui
```

#### Opção 2: Modelo Local (Ollama)

1. Instale o Ollama: https://ollama.ai
2. Baixe um modelo:

```bash
ollama pull llama3.2
```

3. Execute o Ollama (ele roda em `http://localhost:11434` por padrão)

## Uso

### Comando Principal: `generate`

Gera um template a partir de documentos jurídicos.

#### Exemplo Básico

```bash
# Analisar um único documento
minuta-generator generate petição.pdf -o template.html

# Analisar múltiplos documentos similares
minuta-generator generate doc1.pdf doc2.pdf doc3.docx -o template_consolidado.html
```

#### Opções Avançadas

```bash
# Gerar template em DOCX
minuta-generator generate documento.pdf -o template.docx --format docx

# Usar modelo local (Ollama)
minuta-generator generate documento.pdf -o template.html --provider local

# Especificar modelo e temperatura
minuta-generator generate documento.pdf -o template.html \
  --model gemini-2.0-flash-exp \
  --temperature 0.2

# Dar um nome personalizado ao template
minuta-generator generate documento.pdf -o template.html \
  --name "Contestação Trabalhista"
```

### Comando de Análise: `analyze`

Analisa um documento e mostra os padrões identificados sem gerar template.

```bash
# Analisar um documento
minuta-generator analyze petição.pdf

# Com modelo local
minuta-generator analyze petição.pdf --provider local
```

### Parâmetros Completos

#### `generate`

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `INPUT_FILES` | Um ou mais arquivos de entrada | - |
| `--output`, `-o` | Caminho do arquivo de saída | - |
| `--format`, `-f` | Formato de saída (html/docx) | `html` |
| `--name`, `-n` | Nome do template | Nome do primeiro arquivo |
| `--provider` | Provedor de LLM (google/local) | `google` |
| `--api-key` | API key do Google | Variável `GOOGLE_API_KEY` |
| `--model` | Nome do modelo LLM | `gemini-2.0-flash-exp` (Google)<br>`llama3.2` (local) |
| `--base-url` | URL para modelo local | `http://localhost:11434/v1` |
| `--temperature` | Temperatura do LLM | `0.3` |

## Arquitetura

```
minuta_generator/
├── readers/          # Leitores de documentos (PDF, DOCX, HTML)
├── llm/              # Integrações com LLMs (Google, Local)
├── analyzer/         # Análise de padrões com IA
├── templates/        # Geração de templates e placeholders
├── writers/          # Escritores de saída (HTML, DOCX)
├── models.py         # Modelos Pydantic
└── cli.py           # Interface de linha de comando
```

## Fluxo de Funcionamento

1. **Leitura**: Os documentos são lidos e convertidos para texto estruturado
2. **Análise**: O LLM analisa os documentos e identifica:
   - Estrutura comum
   - Padrões repetitivos
   - Partes variáveis (nomes, datas, números, etc.)
   - Tipos de campos (cabeçalho, assinatura, número de processo, etc.)
3. **Geração**: Um template é criado com:
   - Texto fixo mantido como está
   - Partes variáveis substituídas por placeholders `{{NOME_DO_CAMPO}}`
4. **Exportação**: Template salvo em HTML ou DOCX com:
   - Destaque visual dos placeholders
   - Lista de campos variáveis
   - Instruções de uso

## Exemplo de Output

### HTML

O template HTML gerado inclui:
- Visualização do documento com **placeholders destacados em amarelo**
- **Sidebar** com lista de todos os placeholders e suas descrições
- **Tooltip** ao passar o mouse sobre placeholders
- Formatação pronta para impressão

### DOCX

O template DOCX gerado inclui:
- Placeholders **destacados em amarelo** e **negrito**
- Anotações ao lado de cada placeholder
- Seção separada com **lista de placeholders**
- Seção de **instruções de uso**
- Metadados sobre documentos originais

## Exemplos de Uso Real

### Caso 1: Template de Contestação

```bash
# Analise 3 contestações similares
minuta-generator generate \
  contestacao1.pdf \
  contestacao2.pdf \
  contestacao3.pdf \
  -o template_contestacao.html \
  --name "Contestação Padrão"
```

**Resultado**: Template com placeholders para:
- `{{NUMERO_PROCESSO}}`
- `{{NOME_REU}}`
- `{{NOME_AUTOR}}`
- `{{VARA}}`
- `{{DATA}}`
- Etc.

### Caso 2: Análise Exploratória

```bash
# Primeiro, analise um documento para ver o que seria identificado
minuta-generator analyze recurso.pdf

# Depois gere o template se estiver satisfeito
minuta-generator generate recurso.pdf -o template.html
```

### Caso 3: Batch Processing

```bash
# Processar todos os PDFs de um diretório
minuta-generator generate *.pdf -o template_consolidado.html
```

## Desenvolvimento

### Estrutura de Código

- **Pydantic models** em `models.py` para validação de dados
- **Async/await** para chamadas de LLM
- **Tabs** para indentação (seguindo padrão do projeto)
- **Type hints** modernos (Python 3.11+)

### Testes

```bash
# Instalar dependências de desenvolvimento
uv pip install -e ".[dev]"

# Executar testes (quando disponíveis)
pytest -vxs tests/

# Type checking
pyright

# Linting e formatação
ruff check --fix
ruff format
```

## Limitações e Considerações

- **Qualidade da análise** depende da qualidade do LLM usado
- **Documentos muito diferentes** podem não gerar templates úteis (use documentos similares)
- **OCR**: PDFs escaneados precisam de OCR prévio
- **Formatação complexa**: Tabelas e layouts complexos podem não ser preservados perfeitamente

## Roadmap

- [ ] Suporte para mais formatos de entrada (ODT, RTF)
- [ ] Interface web para upload e visualização
- [ ] Templates pré-definidos para tipos comuns de documentos
- [ ] Integração com sistemas de gestão processual
- [ ] Fine-tuning de modelos para domínio jurídico brasileiro
- [ ] Suporte para cláusulas opcionais/condicionais
- [ ] Validação de preenchimento de templates

## Suporte e Contribuições

Para reportar bugs, sugerir features ou contribuir:

1. Abra uma issue descrevendo o problema/sugestão
2. Para contribuições, faça um fork e abra um Pull Request
3. Siga os padrões de código do projeto (tabs, type hints, etc.)

## Licença

[Definir licença apropriada]

## Autores

Desenvolvido pela equipe de Legal Tech da PGM.
