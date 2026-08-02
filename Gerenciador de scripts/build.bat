@echo off
echo Iniciando build do Gerenciador de Scripts com PyInstaller...
py -m pip install -r requirements.txt
py -m pip install pyinstaller

echo Compilando...
py -m PyInstaller --noconfirm --onedir --windowed --icon "icone_geogis.png" --name "Gerenciador_Geogis" --add-data "frontend;frontend/" --add-data "backend;backend/" --add-data "config;config/" --add-data "icone_geogis.png;."  "main.py"

echo Build finalizado! O executavel esta na pasta dist/Gerenciador_Geogis
pause
