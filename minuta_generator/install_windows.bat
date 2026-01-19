@echo off
REM Script de instalação do Minuta Generator para Windows
REM Execute este arquivo no diretório onde você extraiu o projeto

echo ========================================
echo   Minuta Generator - Instalação
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Por favor, instale Python 3.11 ou superior de: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação
    pause
    exit /b 1
)

echo [OK] Python encontrado:
python --version
echo.

REM Verificar se uv está instalado, senão instalar
echo Verificando uv (gerenciador de pacotes)...
uv --version >nul 2>&1
if errorlevel 1 (
    echo uv não encontrado. Instalando uv...
    python -m pip install uv
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar uv
        pause
        exit /b 1
    )
)

echo [OK] uv encontrado
echo.

REM Criar ambiente virtual
echo Criando ambiente virtual...
uv venv --python 3.11
if errorlevel 1 (
    echo [ERRO] Falha ao criar ambiente virtual
    pause
    exit /b 1
)
echo [OK] Ambiente virtual criado
echo.

REM Ativar ambiente e instalar dependências
echo Instalando dependências...
call .venv\Scripts\activate.bat
uv pip install -e .
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Instalação Concluída com Sucesso!
echo ========================================
echo.
echo Próximos passos:
echo.
echo 1. Configure sua API key do Google Gemini:
echo    Copie .env.example para .env e adicione sua chave
echo.
echo 2. Ative o ambiente virtual:
echo    .venv\Scripts\activate.bat
echo.
echo 3. Execute o programa:
echo    minuta-generator --help
echo.
echo Consulte README_WINDOWS.md para mais informações
echo.
pause
