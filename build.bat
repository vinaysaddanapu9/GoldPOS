@echo off
echo ============================
echo Building GoldPOS Portable
echo ============================

REM Go to project folder
cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo.
echo Building GoldPOS EXE...
echo.

REM Clean previous build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build EXE
python -m PyInstaller --clean --onefile --windowed --name GoldPOS --icon=assets\goldpos.ico main.py

if errorlevel 1 (
    echo.
    echo ============================
    echo BUILD FAILED
    echo ============================
    pause
    exit /b 1
)

REM Create portable folder
if exist GoldPOS_Portable rmdir /s /q GoldPOS_Portable

mkdir GoldPOS_Portable
mkdir GoldPOS_Portable\data
mkdir GoldPOS_Portable\data\daily_sales
mkdir GoldPOS_Portable\data\backups

REM Copy EXE
copy dist\GoldPOS.exe GoldPOS_Portable\

REM Copy config
copy config.json GoldPOS_Portable\

echo.
echo ============================
echo Portable package created!
echo ============================
echo.
echo Location:
echo %CD%\GoldPOS_Portable
echo.

pause