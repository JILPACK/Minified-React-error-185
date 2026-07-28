;==============================================================================
; Fichier:   pit.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Programmable Interval Timer (PIT 8253)
;
; Le PIT genere une interruption periodique (IRQ0).
; Configuration :
;   - Canal 0 : Timer systeme (100 Hz)
;   - Canal 1 : Reserve (DRAM refresh)
;   - Canal 2 : PC Speaker
;==============================================================================

PIT_FREQ            equ 1193180    ; Frequence de base du PIT (1.19318 MHz)

;======================================================================
; pit_init - Initialise le timer PIT canal 0 a 100 Hz
;
; Diviseur = PIT_FREQ / frequence_desiree
; Pour 100 Hz : diviseur = 1193180 / 100 = 11931 (0x2E9B)
;======================================================================
pit_init:
    push ax

    cli

    ; Canal 0, mode 2 (rate generator), 16-bit binary
    mov al, 0x34                ; 00 11 010 0 = canal 0, lobyte/hibyte, mode 2, binary
    out PIT_CMD, al
    call pic_io_delay

    ; Charger le diviseur pour 100 Hz
    mov ax, 11931               ; 1193180 / 100 = ~11931
    out PIT_CH0, al             ; Octet bas
    call pic_io_delay
    mov al, ah
    out PIT_CH0, al             ; Octet haut
    call pic_io_delay

    sti

    pop ax
    ret

;======================================================================
; pit_set_freq - Change la frequence du PIT
; Entree:  AX = nouvelle frequence (Hz)
;======================================================================
pit_set_freq:
    push ax
    push bx
    push dx

    cli

    ; Verifier que AX > 0
    test ax, ax
    jz .done

    ; Calculer le diviseur = PIT_FREQ / frequence
    push ax
    mov dx, 0
    mov ax, PIT_FREQ & 0xFFFF
    mov bx, [esp]               ; Frequence
    div bx                      ; AX = diviseur
    add sp, 2

    ; Canal 0, mode 2
    mov al, 0x34
    out PIT_CMD, al
    call pic_io_delay

    ; Envoyer le diviseur
    out PIT_CH0, al
    call pic_io_delay
    mov al, ah
    out PIT_CH0, al
    call pic_io_delay

.done:
    sti

    pop dx
    pop bx
    pop ax
    ret

;======================================================================
; pit_get_count - Lit le compteur actuel du PIT
; Sortie:  AX = valeur actuelle du compteur
;======================================================================
pit_get_count:
    push dx

    cli

    ; Verrouiller le compteur (latch command)
    mov al, 0x00                ; Canal 0, latch
    out PIT_CMD, al
    call pic_io_delay

    ; Lire la valeur
    in al, PIT_CH0              ; Octet bas
    mov dl, al
    call pic_io_delay
    in al, PIT_CH0              ; Octet haut
    mov dh, al

    mov ax, dx

    sti

    pop dx
    ret

;======================================================================
; pit_ms_delay - Attente en millisecondes (approximatif)
; Entree:  AX = millisecondes
;======================================================================
pit_ms_delay:
    push ax
    push bx

    ; Utiliser le compteur de ticks du timer
    ; A 100 Hz, 1 tick = 10 ms
    mov bl, 10
    div bl                      ; AL = ticks (arrondi)
    cmp al, 0
    jne .do_delay
    inc al                      ; Minimum 1 tick

.do_delay:
    xor ah, ah
    call sleep                  ; Attendre AL ticks

    pop bx
    pop ax
    ret

;======================================================================
; pic_io_delay - Petit delai pour operations PIC/PIT (redef pour pit.asm)
;======================================================================
pic_io_delay:
    push ax
    mov al, 0
    out 0x80, al
    pop ax
    ret
