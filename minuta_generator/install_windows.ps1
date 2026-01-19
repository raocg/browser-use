# Script de instalação do Minuta Generator para Windows (PowerShell)
# Execute: .\install_windows.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Minuta Generator - Instalação" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Python não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale Python 3.11 ou superior de: https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Certifique-se de marcar 'Add Python to PATH' durante a instalação" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host ""

# Verificar versão do Python
$versionMatch = $pythonVersion -match '(\d+)\.(\d+)\.(\d+)'
if ($versionMatch) {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]

    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
        Write-Host "[AVISO] Python $major.$minor detectado. Recomendado: Python 3.11+" -ForegroundColor Yellow
        $continue = Read-Host "Continuar mesmo assim? (s/N)"
        if ($continue -ne 's' -and $continue -ne 'S') {
            exit 0
        }
    }
}

# Verificar se uv está instalado
Write-Host "Verificando uv (gerenciador de pacotes)..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version 2>&1
    Write-Host "[OK] uv encontrado" -ForegroundColor Green
} catch {
    Write-Host "uv não encontrado. Instalando..." -ForegroundColor Yellow
    python -m pip install uv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao instalar uv" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
    Write-Host "[OK] uv instalado com sucesso" -ForegroundColor Green
}
Write-Host ""

# Criar ambiente virtual
Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
uv venv --python 3.11
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao criar ambiente virtual" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "[OK] Ambiente virtual criado em .venv\" -ForegroundColor Green
Write-Host ""

# Ativar ambiente e instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
uv pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao instalar dependências" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "[OK] Dependências instaladas" -ForegroundColor Green
Write-Host ""

# Verificar se .env existe
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "Criando arquivo .env a partir de .env.example..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "[OK] Arquivo .env criado" -ForegroundColor Green
        Write-Host ""
        Write-Host "[IMPORTANTE] Edite o arquivo .env e adicione sua GOOGLE_API_KEY" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Instalação Concluída com Sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Próximos passos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure sua API key do Google Gemini:" -ForegroundColor White
Write-Host "   Edite o arquivo .env e adicione sua chave" -ForegroundColor Gray
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Ative o ambiente virtual:" -ForegroundColor White
Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""

Write-Host "3. Execute o programa:" -ForegroundColor White
Write-Host "   minuta-generator --help" -ForegroundColor Gray
Write-Host ""

Write-Host "4. Exemplo de uso:" -ForegroundColor White
Write-Host '   minuta-generator generate "documento.pdf" -o template.html' -ForegroundColor Gray
Write-Host ""

Write-Host "Consulte README_WINDOWS.md para mais informações" -ForegroundColor Cyan
Write-Host ""

# Testar instalação
Write-Host "Testando instalação..." -ForegroundColor Yellow
try {
    $helpOutput = minuta-generator --help 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Comando minuta-generator está funcionando!" -ForegroundColor Green
    } else {
        Write-Host "[AVISO] Comando pode não estar no PATH. Use:" -ForegroundColor Yellow
        Write-Host "  .\.venv\Scripts\minuta-generator.exe" -ForegroundColor Gray
    }
} catch {
    Write-Host "[AVISO] Teste do comando falhou. Ative o ambiente primeiro:" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
}
Write-Host ""

Read-Host "Pressione Enter para sair"
