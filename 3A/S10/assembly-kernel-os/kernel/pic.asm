;==============================================================================
; Fichier:   pic.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Programmable Interrupt Controller (PIC 8259A)
;
; Le PIC gere les interruptions materielles (IRQ).
; Configuration :
;   - PIC maitre : IRQ0-7  -> INT 0x20-0x27
;   - PIC esclave : IRQ8-15 -> INT 0x28-0x2F
;==============================================================================

;======================================================================
; pic_init - Initialise les deux PICs (maitre et esclave)
;
; Les IRQ sont remappees des vecteurs BIOS (0x08-0x0F) vers
; les vecteurs 0x20-0x2F pour eviter les conflits avec les
; exceptions CPU (0x00-0x1F).
;======================================================================
pic_init:
    push ax

    cli

    ; Initialisation du PIC maitre (ICW1)
    mov al, 0x11                ; ICW1: ICW4 needed, cascade mode, edge triggered
    out PIC1_CMD, al
    call io_delay

    ; ICW2: Vecteur de base pour IRQ0-7 (0x20 = INT 0x20-0x27)
    mov al, 0x20
    out PIC1_DATA, al
    call io_delay

    ; ICW3: Maitre a IRQ2 pour l'esclave
    mov al, 0x04                ; Slave connecte a IRQ2 (bit 2)
    out PIC1_DATA, al
    call io_delay

    ; ICW4: Mode 8086, EOI normal
    mov al, 0x01
    out PIC1_DATA, al
    call io_delay

    ; Initialisation du PIC esclave (ICW1)
    mov al, 0x11
    out PIC2_CMD, al
    call io_delay

    ; ICW2: Vecteur de base pour IRQ8-15 (0x28 = INT 0x28-0x2F)
    mov al, 0x28
    out PIC2_DATA, al
    call io_delay

    ; ICW3: Cascade ID = 2 (se connecte a IRQ2 du maitre)
    mov al, 0x02
    out PIC2_DATA, al
    call io_delay

    ; ICW4: Mode 8086, EOI normal
    mov al, 0x01
    out PIC2_DATA, al
    call io_delay

    ; Masquer toutes les IRQ sauf IRQ0 (timer) et IRQ1 (clavier)
    mov al, 0xFC                ; IRQ0 et IRQ1 actives, IRQ2-7 masquees
    out PIC1_DATA, al
    call io_delay

    mov al, 0xFF                ; Toutes les IRQ8-15 masquees
    out PIC2_DATA, al
    call io_delay

    sti

    pop ax
    ret

;======================================================================
; io_delay - Petit delai pour les operations E/S
;======================================================================
io_delay:
    push ax
    mov al, 0
    out 0x80, al                ; Port inutilise pour delai
    pop ax
    ret

;======================================================================
; pic_enable_irq - Active une IRQ specifique
; Entree:  AL = numero d'IRQ (0-15)
;======================================================================
pic_enable_irq:
    push ax
    push bx
    push dx

    mov bl, al
    cmp al, 8
    jb .master

    ; IRQ 8-15 sur PIC esclave
    sub bl, 8
    in al, PIC2_DATA
    call clear_bit_al_bl
    out PIC2_DATA, al
    jmp .done

.master:
    ; IRQ 0-7 sur PIC maitre
    in al, PIC1_DATA
    call clear_bit_al_bl
    out PIC1_DATA, al

.done:
    pop dx
    pop bx
    pop ax
    ret

;======================================================================
; clear_bit_al_bl - Efface le bit BL dans AL
; Entree:  AL = valeur, BL = position du bit (0-7)
; Sortie:  AL = valeur modifiee
;======================================================================
clear_bit_al_bl:
    push cx
    mov cl, bl
    mov ah, 1
    shl ah, cl                  ; AH = 1 << BL
    not ah                      ; AH = ~(1 << BL)
    and al, ah
    pop cx
    ret

;======================================================================
; set_bit_al_bl - Met le bit BL dans AL
; Entree:  AL = valeur, BL = position du bit (0-7)
; Sortie:  AL = valeur modifiee
;======================================================================
set_bit_al_bl:
    push cx
    mov cl, bl
    mov ah, 1
    shl ah, cl                  ; AH = 1 << BL
    or al, ah
    pop cx
    ret

;======================================================================
; pic_disable_irq - Desactive une IRQ specifique
; Entree:  AL = numero d'IRQ (0-15)
;======================================================================
pic_disable_irq:
    push ax
    push bx
    push dx

    mov bl, al
    cmp al, 8
    jb .master

    ; IRQ 8-15 sur PIC esclave
    sub bl, 8
    in al, PIC2_DATA
    call set_bit_al_bl
    out PIC2_DATA, al
    jmp .done

.master:
    ; IRQ 0-7 sur PIC maitre
    in al, PIC1_DATA
    call set_bit_al_bl
    out PIC1_DATA, al

.done:
    pop dx
    pop bx
    pop ax
    ret

;======================================================================
; pic_send_eoi - Envoie un EOI (End of Interrupt)
; Entree:  AL = numero d'IRQ
;======================================================================
pic_send_eoi:
    push ax

    cmp al, 8
    jb .master

    ; EOI pour PIC esclave
    mov al, 0x20
    out PIC2_CMD, al

.master:
    ; EOI pour PIC maitre
    mov al, 0x20
    out PIC1_CMD, al

    pop ax
    ret
