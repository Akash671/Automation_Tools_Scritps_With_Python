@echo off

:GET_SCRIPT_NAME

echo Enter the name of the Python script (e.g., main.py):
set /p script_name=

if not defined script_name (
  echo Please enter a script name.
  goto GET_SCRIPT_NAME
)

python -m PyInstaller --onefile %script_name%
pause