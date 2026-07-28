#==============================================================================
# Fichier:   Makefile
# Projet:    Assembly Kernel OS - 3AS10 ENSEM NRJ
# Description: Compilation et assemblage du noyau
#
# Utilisation:
#   make all      - Compile le projet complet (boot + kernel)
#   make boot     - Compile uniquement le boot sector
#   make kernel   - Compile le noyau
#   make run      - Lance l'emulateur QEMU
#   make debug    - Lance QEMU avec debug GDB
#   make clean    - Nettoie les fichiers generes
#   make floppy   - Cree une image disquette bootable
#==============================================================================

# Outils
NASM        = nasm
QEMU        = qemu-system-x86_64
DD          = dd
RM          = del /Q
MKDIR       = mkdir

# Options NASM
NASM_FLAGS  = -f bin -I.

# Fichiers source
BOOT_SRC    = boot/boot.asm
KERNEL_SRC  = kernel/start.asm
LINK_SCRIPT = kernel.ld

# Fichiers objets
BOOT_BIN    = build/boot.bin
KERNEL_BIN  = build/kernel.bin
OS_IMG      = build/os-image.bin
FLOPPY_IMG  = build/floppy.img

# Options QEMU
QEMU_FLAGS  = -m 64 -drive format=raw,file=$(OS_IMG),if=floppy
QEMU_DEBUG  = -s -S

#==============================================================================
# Cibles principales
#==============================================================================

all: boot kernel image

# Compilation du boot sector
boot: $(BOOT_SRC) include/kernel.inc
	$(NASM) $(NASM_FLAGS) $(BOOT_SRC) -o $(BOOT_BIN)
	@echo "Boot sector compile: $(BOOT_BIN)"

# Compilation du noyau
kernel: $(KERNEL_SRC) drivers/screen.asm drivers/keyboard.asm kernel/isr.asm kernel/pic.asm kernel/pit.asm kernel/shell.asm lib/string.asm lib/stdio.asm include/kernel.inc
	$(NASM) $(NASM_FLAGS) $(KERNEL_SRC) -o $(KERNEL_BIN)
	@echo "Noyau compile: $(KERNEL_BIN)"
	@echo "Taille du noyau: $$(wc -c < $(KERNEL_BIN)) octets"

# Assemblage de l'image OS (boot + kernel)
image: boot kernel
	copy /b $(BOOT_BIN) + $(KERNEL_BIN) $(OS_IMG)
	@echo "Image OS creee: $(OS_IMG)"
	@echo "Taille totale: $$(wc -c < $(OS_IMG)) octets"

#==============================================================================
# Emulation
#==============================================================================

run: image
	$(QEMU) $(QEMU_FLAGS)

debug: image
	$(QEMU) $(QEMU_FLAGS) $(QEMU_DEBUG)

#==============================================================================
# Image disquette
#==============================================================================

floppy: image
	$(DD) if=/dev/zero of=$(FLOPPY_IMG) bs=512 count=2880
	$(DD) if=$(OS_IMG) of=$(FLOPPY_IMG) conv=notrunc
	@echo "Image disquette creee: $(FLOPPY_IMG)"

#==============================================================================
# Nettoyage
#==============================================================================

clean:
	-$(RM) $(BOOT_BIN) 2>nul
	-$(RM) $(KERNEL_BIN) 2>nul
	-$(RM) $(OS_IMG) 2>nul
	-$(RM) $(FLOPPY_IMG) 2>nul
	@echo "Nettoyage termine."

#==============================================================================
# Utilitaire
#==============================================================================

.PHONY: all boot kernel image run debug floppy clean

info:
	@echo "===== Assembly Kernel OS - Build System ====="
	@echo "NASM:    $(shell where $(NASM) 2>nul || echo NON TROUVE)"
	@echo "QEMU:    $(shell where $(QEMU) 2>nul || echo NON TROUVE)"
	@echo ""
	@echo "Cibles disponibles:"
	@echo "  make all    - Compile tout"
	@echo "  make boot   - Compile le boot sector"
	@echo "  make kernel - Compile le noyau"
	@echo "  make image  - Cree l'image OS"
	@echo "  make run    - Lance QEMU"
	@echo "  make debug  - Lance QEMU avec debug"
	@echo "  make clean  - Nettoie les fichiers"
