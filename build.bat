@echo off
pyinstaller --onefile --windowed --name ToDo --add-data "styles;styles" --add-data "Resources;Resources" app.py