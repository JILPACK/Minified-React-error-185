@echo off
REM ============================================================================
REM Fichier:   build.bat
REM Projet:    Assembly Kernel OS - 3AS10 ENSEM NRJ
REM Description: Script de compilation pour Windows
REM ============================================================================

echo ===== Assembly Kernel OS - Build System =====
echo.

REM Verification de NASM
where nasm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] NASM (Netwide Assembler) n'est pas installe!
    echo.
    echo Telechargez NASM depuis: https://www.nasm.us/
    echo Ajoutez nasm.exe a votre PATH.
    echo.
    pause
    exit /b 1
)
echo [OK] NASM trouve

REM Verification de QEMU (optionnel)
where qemu-system-x86_64 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] QEMU trouve
) else (
    echo [AVERTISSEMENT] QEMU non trouve - utilisez QEMU pour emuler l'OS
    echo Telechargez QEMU depuis: https://www.qemu.org/
)
echo.

REM Creation du repertoire build
if not exist build mkdir build

REM ============================================================================
REM Etape 1: Compilation du boot sector
REM ============================================================================
echo Etape 1/3: Compilation du boot sector...
nasm -f bin -I. boot/boot.asm -o build\boot.bin
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Echec de la compilation du boot sector!
    pause
    exit /b 1
)
echo [OK] Boot sector compile (build\boot.bin)

REM ============================================================================
REM Etape 2: Compilation du noyau
REM ============================================================================
echo Etape 2/3: Compilation du noyau...
nasm -f bin -I. kernel/start.asm -o build\kernel.bin
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Echec de la compilation du noyau!
    pause
    exit /b 1
)

REM Verifier la taille du noyau
for %%A in (build\kernel.bin) do set KERNEL_SIZE=%%~zA
echo [OK] Noyau compile (build\kernel.bin - %KERNEL_SIZE% octets)

REM ============================================================================
REM Etape 3: Assemblage de l'image OS
REM ============================================================================
echo Etape 3/3: Assemblage de l'image OS...
copy /b build\boot.bin + build\kernel.bin build\os-image.bin >nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Echec de l'assemblage de l'image!
    pause
    exit /b 1
)

for %%A in (build\os-image.bin) do set IMG_SIZE=%%~zA
echo [OK] Image OS creee (build\os-image.bin - %IMG_SIZE% octets)
echo.

echo ===== Compilation reussie! =====
echo.
echo Pour lancer l'OS avec QEMU:
echo   qemu-system-x86_64 -m 64 -drive format=raw,file=build\os-image.bin,if=floppy
echo.
echo Ou utilisez la cible "run" du Makefile si vous avez GNU Make.
echo.
pause
