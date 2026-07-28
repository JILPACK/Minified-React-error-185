@echo off
REM ============================================================================
REM Fichier:   run.bat
REM Projet:    Assembly Kernel OS - 3AS10 ENSEM NRJ
REM Description: Lance l'OS dans QEMU
REM ============================================================================

echo Assembly Kernel OS - Lancement QEMU
echo.

REM Verifier que l'image existe
if not exist build\os-image.bin (
    echo [ERREUR] Image OS non trouvee. Lancez build.bat d'abord.
    pause
    exit /b 1
)

REM Verifier que QEMU est installe
where qemu-system-x86_64 >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] QEMU n'est pas installe!
    echo.
    echo Telechargez QEMU depuis: https://www.qemu.org/
    echo et ajoutez-le a votre PATH.
    pause
    exit /b 1
)

echo Lancement de Assembly Kernel OS...
echo.
echo Commandes disponibles dans le shell:
echo   help, cls, echo, time, ticks, color, beep
echo   info, reset, mem, calc, demo
echo.
echo Appuyez sur Ctrl+Alt+G pour liberer la souris QEMU.
echo.
qemu-system-x86_64 -m 64 -drive format=raw,file=build\os-image.bin,if=floppy

if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] QEMU s'est arrete avec une erreur.
    pause
)
