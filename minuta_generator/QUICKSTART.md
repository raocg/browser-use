# Guia Rápido - Minuta Generator

## Instalação em 3 passos

```bash
# 1. Navegue até o diretório
cd minuta_generator

# 2. Crie ambiente e instale
uv venv --python 3.11
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .

# 3. Configure sua API key do Google
export GOOGLE_API_KEY="sua-chave-aqui"
```

## Uso Básico

### Gerar template de um documento

```bash
minuta-generator generate documento.pdf -o template.html
```

Abra `template.html` no navegador para ver o resultado!

### Gerar template de vários documentos similares

```bash
minuta-generator generate doc1.pdf doc2.pdf doc3.docx -o template.html
```

### Gerar em formato DOCX

```bash
minuta-generator generate documento.pdf -o template.docx --format docx
```

### Analisar antes de gerar

```bash
# Veja o que será identificado
minuta-generator analyze documento.pdf

# Se estiver bom, gere o template
minuta-generator generate documento.pdf -o template.html
```

## Usar modelo local (sem API key)

1. Instale Ollama: https://ollama.ai
2. Baixe um modelo:
   ```bash
   ollama pull llama3.2
   ```
3. Execute:
   ```bash
   minuta-generator generate documento.pdf -o template.html --provider local
   ```

## Dicas

- **Documentos similares**: Use documentos do mesmo tipo (ex: 3 contestações) para melhores resultados
- **Formato HTML**: Melhor para visualização e apresentação
- **Formato DOCX**: Melhor para edição e preenchimento
- **API Key**: Guarde em `.env` em vez de exportar toda vez

## Solução de Problemas

### "Google API key é necessária"
```bash
export GOOGLE_API_KEY="sua-chave"
# Ou crie arquivo .env com: GOOGLE_API_KEY=sua-chave
```

### "Unsupported file format"
Formatos suportados: `.pdf`, `.docx`, `.html`

### Modelo local não conecta
Verifique se Ollama está rodando:
```bash
ollama list  # Deve mostrar modelos instalados
```

## Próximos Passos

- Leia o [README.md](README.md) completo para detalhes
- Veja [example_usage.py](example_usage.py) para uso programático
- Experimente diferentes temperaturas (`--temperature 0.1` a `0.7`)
- Teste com seus documentos reais!

## Ajuda

```bash
# Ver todos os comandos
minuta-generator --help

# Ajuda de um comando específico
minuta-generator generate --help
```
