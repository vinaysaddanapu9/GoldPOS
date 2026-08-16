@echo off
echo ============================
echo Building GoldPOS Portable
echo ============================

REM Go to project folder
cd /d %~dp0src

REM Build EXE
python -m pyinstaller --onefile --windowed --name GoldPOS --icon=assets\goldpos.ico src\main.py

REM Create portable folder
cd ..

if exist GoldPOS_Portable rmdir /s /q GoldPOS_Portable

mkdir GoldPOS_Portable
mkdir GoldPOS_Portable\data
mkdir GoldPOS_Portable\data\daily_sales
mkdir GoldPOS_Portable\data\backups

copy src\dist\GoldPOS.exe GoldPOS_Portable\
copy src\config.json GoldPOS_Portable\

echo.
echo ============================
echo Portable package created!
echo ============================
echo Location: GoldPOS_Portable
pause


