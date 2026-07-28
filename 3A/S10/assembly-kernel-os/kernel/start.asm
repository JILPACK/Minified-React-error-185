;==============================================================================
; Fichier:   start.asm
; Projet:    Assembly Kernel OS - 3AS10
; Auteur:    ENSEM NRJ (FISA)
; Description: Point d'entree du noyau - initialisation du systeme
;
; Ce module initialise :
; 1. Les segments et la pile en mode protege
; 2. La memoire video VGA
; 3. Les interruptions (IDT, PIC, ISR)
; 4. Le timer PIT
; 5. Le shell utilisateur
;==============================================================================

; Inclure les definitions du noyau
%include 'include/kernel.inc'

[BITS 16]                       ; Demarrage en mode reel
[ORG 0x0000]                    ; ORG = 0 car segment 0x1000

;======================================================================
; Point d'entree - appele par le bootloader
; DL = lecteur de boot
;======================================================================
global _start
_start:
    ; Configurer les segments pour le noyau
    cli
    mov ax, cs
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0xFFFE               ; Pile en haut du segment
    sti

    ; Sauvegarder le lecteur de boot
    mov [boot_device], dl

    ; Initialiser l'ecran (mode texte 80x25)
    call screen_init

    ; Afficher la banniere de demarrage
    mov si, banner_line1
    call screen_puts_attr
    call screen_newline
    mov si, banner_line2
    call screen_puts_attr
    call screen_newline
    mov si, banner_line3
    call screen_puts_attr
    call screen_newline
    mov si, banner_line4
    call screen_puts_attr
    call screen_newline
    mov si, banner_line5
    call screen_puts_attr
    call screen_newline

    ; Initialiser le PIC (Programmable Interrupt Controller)
    call pic_init

    ; Initialiser les ISR (Interrupt Service Routines)
    call isr_init

    ; Initialiser le timer PIT a 100 Hz
    call pit_init

    ; Activer les interruptions
    sti

    ; Afficher le message de bienvenue
    call screen_newline
    mov si, msg_welcome
    call screen_puts_attr
    call screen_newline

    ; Afficher les informations systeme
    call display_sysinfo
    call screen_newline

    ; Demarrer le shell
    mov si, msg_start_shell
    call screen_puts_attr
    call screen_newline
    call shell_start

;======================================================================
; display_sysinfo - Affiche les informations du systeme
;======================================================================
display_sysinfo:
    push si
    push ax
    push bx

    mov si, msg_cpu_mode
    call screen_puts_attr
    call screen_newline

    mov si, msg_memory
    call screen_puts_attr
    call screen_newline

    mov si, msg_version
    call screen_puts_attr
    call screen_newline

    pop bx
    pop ax
    pop si
    ret

;======================================================================
; halt - Arret du systeme (jamais atteint normalement)
;======================================================================
halt:
    cli
    hlt
    jmp halt

;======================================================================
; Donnees
;================================================================------
boot_device         db 0

banner_line1        db ATTR_CYAN_ON_BLACK, '================================================', 0
banner_line2        db ATTR_CYAN_ON_BLACK, '     Assembly Kernel OS v1.0 - 3AS10 ENSEM NRJ     ', 0
banner_line3        db ATTR_CYAN_ON_BLACK, '================================================', 0
banner_line4        db ATTR_GREEN_ON_BLACK, 'Noyau en assembleur x86 - Mode reel 16 bits', 0
banner_line5        db ATTR_CYAN_ON_BLACK, '================================================', 0

msg_welcome         db ATTR_YELLOW_ON_BLACK, 'Bienvenue dans Assembly Kernel OS!', 0
msg_cpu_mode        db ATTR_WHITE_ON_BLACK, 'Mode CPU: x86-16 bits (Mode reel)', 0
msg_memory          db ATTR_WHITE_ON_BLACK, 'Memoire:  1 Mo accessible (20 bits)', 0
msg_version         db ATTR_WHITE_ON_BLACK, 'Version:  1.0 - Projet 3AS10', 0
msg_start_shell     db ATTR_GREEN_ON_BLACK, 'Demarrage du shell...', 0

; Inclure les modules du noyau
%include 'drivers/screen.asm'
%include 'drivers/keyboard.asm'
%include 'kernel/isr.asm'
%include 'kernel/pic.asm'
%include 'kernel/pit.asm'
%include 'kernel/shell.asm'
%include 'lib/string.asm'
%include 'lib/stdio.asm'
