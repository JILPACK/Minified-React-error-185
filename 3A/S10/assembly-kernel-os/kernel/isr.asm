;==============================================================================
; Fichier:   isr.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Gestionnaires d'interruptions (ISR)
;
; Interruptions gerees :
;   0x00 - Division par zero
;   0x20 - IRQ0 (Timer PIT)
;   0x21 - IRQ1 (Clavier)
;   0x22-0x27 - IRQ2-7
;   0x28-0x2F - IRQ8-15
;==============================================================================

;--------- Compteur de ticks pour le timer ---------
timer_ticks         dw 0        ; Compteur de ticks (incremente a chaque IRQ0)
timer_seconds       db 0        ; Secondes ecoulees

;======================================================================
; isr_init - Initialise la table des vecteurs d'interruption (IVT)
; On remplace les vecteurs du BIOS par nos propres handlers
; NOTE: En mode reel, l'IVT se trouve a l'adresse 0x0000-0x03FF
;======================================================================
isr_init:
    push ax
    push bx
    push es
    push ds

    cli

    ; Desactiver toutes les interruptions IRQ du PIC
    mov al, 0xFF
    out PIC1_DATA, al
    out PIC2_DATA, al

    ; Remplacer les vecteurs dans l'IVT
    ; Nous devons modifier l'IVT en mode reel (adresse 0)
    xor ax, ax
    mov es, ax
    mov ds, ax

    ; Vector 0x00 - Division par zero
    mov word [es:0x00], isr_div0
    mov [es:0x02], cs

    ; Vector 0x20 - IRQ0 (Timer)
    mov word [es:0x20*4], isr_timer
    mov [es:0x20*4+2], cs

    ; Vector 0x21 - IRQ1 (Clavier)
    mov word [es:0x21*4], isr_keyboard
    mov [es:0x21*4+2], cs

    ; Vector 0x22-0x27 - IRQ2-7 (handler generique)
    mov bx, 0x22 * 4
.irq_loop1:
    mov word [es:bx], isr_spurious
    mov [es:bx+2], cs
    add bx, 4
    cmp bx, 0x28 * 4
    jb .irq_loop1

    ; Vector 0x28-0x2F - IRQ8-15 (handler generique)
    mov bx, 0x28 * 4
.irq_loop2:
    mov word [es:bx], isr_spurious
    mov [es:bx+2], cs
    add bx, 4
    cmp bx, 0x30 * 4
    jb .irq_loop2

    sti

    pop ds
    pop es
    pop bx
    pop ax
    ret

;======================================================================
; isr_div0 - Gestionnaire de division par zero
;======================================================================
isr_div0:
    push ax
    push si
    push ds

    mov ax, cs
    mov ds, ax

    mov si, msg_div0
    call screen_puts_attr
    call screen_newline

    ; Boucle infinie (arret securitaire)
.halt:
    hlt
    jmp .halt

    pop ds
    pop si
    pop ax
    iret

;======================================================================
; isr_timer - Gestionnaire IRQ0 (Timer PIT - ~18.2 Hz par defaut)
;======================================================================
isr_timer:
    push ax
    push ds

    mov ax, cs
    mov ds, ax

    ; Incrementer le compteur de ticks
    inc word [timer_ticks]

    ; Toutes les ~18 ticks (~1 seconde)
    mov ax, [timer_ticks]
    and ax, 0x000F              ; Compter 16 ticks
    jnz .done

    inc byte [timer_seconds]

.done:
    ; Acquitter l'interruption aupres du PIC
    mov al, 0x20
    out PIC1_CMD, al

    pop ds
    pop ax
    iret

;======================================================================
; isr_keyboard - Gestionnaire IRQ1 (Clavier)
; Delegue a kb_handler dans keyboard.asm
;======================================================================
isr_keyboard:
    ; Sauter au gestionnaire du clavier
    jmp kb_handler
    ; Note: kb_handler se termine par iret

;======================================================================
; isr_spurious - Gestionnaire pour les interruptions non utilisees
;======================================================================
isr_spurious:
    push ax

    ; Acquitter l'interruption
    mov al, 0x20
    out PIC1_CMD, al

    pop ax
    iret

;======================================================================
; isr_get_ticks - Retourne le nombre de ticks timer
; Sortie:  AX = ticks
;======================================================================
isr_get_ticks:
    push ds
    mov ax, cs
    mov ds, ax
    mov ax, [timer_ticks]
    pop ds
    ret

;======================================================================
; isr_get_seconds - Retourne les secondes ecoulees
; Sortie:  AX = secondes
;======================================================================
isr_get_seconds:
    push ds
    mov ax, cs
    mov ds, ax
    xor ah, ah
    mov al, [timer_seconds]
    pop ds
    ret

;======================================================================
; sleep - Attend un nombre donne de ticks
; Entree:  AX = nombre de ticks a attendre
;======================================================================
sleep:
    push bx
    push ds

    mov bx, cs
    mov ds, bx
    cli
    mov bx, [timer_ticks]
    add bx, ax                  ; BX = tick cible
    sti

.wait:
    sti
    nop
    cli
    cmp [timer_ticks], bx
    jb .wait

    sti
    pop ds
    pop bx
    ret

;======================================================================
; Donnees
;======================================================================
msg_div0            db ATTR_RED_ON_BLACK, 'ERREUR FATALE: Division par zero!', 0
