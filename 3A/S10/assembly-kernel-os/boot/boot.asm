;==============================================================================
; Fichier:   boot.asm
; Projet:    Assembly Kernel OS - 3AS10
; Auteur:    ENSEM NRJ (FISA)
; Description: Boot sector (stage 1) - Charge le noyau depuis le disque
;
; Ce boot sector :
; 1. Initialise les segments et la pile
; 2. Charge le noyau depuis le disque (secteurs 2+)
; 3. Passe en mode protege (optionnel)
; 4. Saute au noyau
;==============================================================================

[BITS 16]
[ORG 0x7C00]                    ; Adresse de chargement du boot sector

;======================================================================
; Boot Sector Entry Point
;======================================================================
start:
    ; Initialisation des segments
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00              ; Pile sous le boot sector
    sti

    ; Sauvegarde du lecteur de boot
    mov [boot_drive], dl

    ; Affichage du message de demarrage
    mov si, msg_booting
    call print_string_16

    ; Chargement du noyau depuis le disque
    mov si, msg_loading_kernel
    call print_string_16

    mov dl, [boot_drive]        ; Lecteur
    mov dh, 0                   ; Tete 0
    mov ch, 0                   ; Cylindre 0
    mov cl, 2                   ; Secteur de depart (secteur 2)
    mov bx, KERNEL_ADDR         ; Destination (0x1000)
    mov al, KERNEL_SECTORS      ; Nombre de secteurs a lire

    call load_sectors

    ; Verification du chargement
    test al, al
    jz load_error

    ; Succes - affichage et saut au noyau
    mov si, msg_done
    call print_string_16
    call print_newline_16

    ; Transfert au noyau
    mov dl, [boot_drive]        ; Passage du lecteur
    mov ax, KERNEL_ADDR
    jmp 0x1000:0x0000           ; Saut far au noyau

;======================================================================
; load_sectors - Charge des secteurs depuis le disque (INT 13h AH=02h)
; Entree:  AL = nombre de secteurs
;          CH = cylindre
;          CL = secteur
;          DH = tete
;          DL = lecteur
;          BX = destination
; Sortie:  AL = 0 si succes, nombre de secteurs lus sinon
;======================================================================
load_sectors:
    push ax
    push bx
    push cx
    push dx
    push es

    mov ax, KERNEL_SEG
    mov es, ax
    xor bx, bx                  ; ES:BX = segment:offset

    mov ah, 0x02                ; Fonction lecture
    int 0x13                    ; Appel BIOS

    jnc .success
    ; Erreur - reessayer
    xor ax, ax
    int 0x13                    ; Reset disque
    pop es
    pop dx
    pop cx
    pop bx
    pop ax
    jmp load_sectors            ; Reessayer

.success:
    pop es
    pop dx
    pop cx
    pop bx
    pop ax
    ret

;======================================================================
; print_string_16 - Affiche une chaine en mode 16 bits (INT 10h)
; Entree:  SI = adresse de la chaine (terminee par 0)
;======================================================================
print_string_16:
    push ax
    push si
    cld
.loop:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0E                ; Fonction teletype
    xor bx, bx
    int 0x10
    jmp .loop
.done:
    pop si
    pop ax
    ret

;======================================================================
; print_newline_16 - Nouvelle ligne en mode 16 bits
;======================================================================
print_newline_16:
    push ax
    mov ah, 0x0E
    mov al, 0x0D                ; CR
    int 0x10
    mov al, 0x0A                ; LF
    int 0x10
    pop ax
    ret

;======================================================================
; load_error - Gestion d'erreur de chargement
;======================================================================
load_error:
    mov si, msg_load_error
    call print_string_16
    call print_newline_16
.halt:
    hlt
    jmp .halt

;======================================================================
; Donnees
;======================================================================
boot_drive          db 0
KERNEL_ADDR         equ 0x1000
KERNEL_SEG          equ 0x1000
KERNEL_SECTORS      equ 32          ; ~16 KB pour le noyau

msg_booting         db 'Assembly Kernel OS - 3AS10 ENSEM NRJ', 0x0D, 0x0A, 0
msg_loading_kernel  db 'Chargement du noyau... ', 0
msg_done            db '[OK]', 0
msg_load_error      db '[ERREUR] Impossible de charger le noyau!', 0

;======================================================================
; Signature du boot sector (55 AA)
;======================================================================
times 510 - ($ - $$) db 0
dw 0xAA55
