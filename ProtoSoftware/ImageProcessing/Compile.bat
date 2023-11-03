@ECHO OFF
ECHO [== COMPILING IMAGE PROCESSING SCRIPT ==]
pyinstaller --onefile ImageProcessingClient.py

IF %ERRORLEVEL% NEQ 0 PAUSE