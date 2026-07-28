;==============================================================================
; Fichier:   keyboard.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Pilote du clavier via IRQ1
;
; Points cles :
;   - Gestion de l'interruption IRQ1 (INT 0x21)
;   - Buffer circulaire pour les touches
;   - Gestion des combinaisons Shift, Caps Lock
;   - Map des touches AZERTY (disposition francaise)
;==============================================================================

;--------- Variables du pilote clavier ---------
kb_buffer           times 256 db 0     ; Buffer circulaire (256 octets)
kb_buffer_head      db 0               ; Index de lecture
kb_buffer_tail      db 0               ; Index d'ecriture
kb_shift_state      db 0               ; 1 = shift enfonce
kb_caps_state       db 0               ; 1 = caps lock actif
kb_last_scancode    db 0               ; Dernier scancode recu

; Table de conversion scancode -> caractere AZERTY (sans shift)
; Seuls les scancodes 0x01-0x53 sont definis
keymap_normal       db 0, 0, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 0, 0, 0, 0
                    db '&', 'e', '"', "'", '(', '-', 'e', '_', 'c', 'a', '^', 0, 0, 0, 0, 0
                    db 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 0, 0, 0, 0, 0, 0
                    db 0, 'w', 'x', 'c', 'v', 'b', 'n', ',', ';', ':', '!', 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, ' ', 0, 0, 0, 0, 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

; Table de conversion scancode -> caractere AZERTY (avec shift)
keymap_shift        db 0, 0, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 0, 0, 0, 0
                    db '1', 'E', '"', "'", '(', '-', 'E', '_', 'C', 'A', '^', 0, 0, 0, 0, 0
                    db 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 0, 0, 0, 0, 0, 0
                    db 0, 'W', 'X', 'C', 'V', 'B', 'N', '?', '.', '/', 0, 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, ' ', 0, 0, 0, 0, 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

;======================================================================
; kb_handler - Gestionnaire d'interruption IRQ1 (INT 0x21)
;======================================================================
kb_handler:
    push ax
    push bx
    push si
    push ds

    ; Configurer DS pour acceder aux donnees du noyau
    mov ax, cs
    mov ds, ax

    ; Lire le scancode depuis le port clavier
    in al, KB_DATA_PORT
    mov [kb_last_scancode], al

    ; Verifier si c'est une touche relachee
    test al, KEY_RELEASED
    jnz .key_released

    ; Touche enfoncee - traiter
    ; Verifier si c'est une touche speciale
    cmp al, KEY_LSHIFT
    je .shift_pressed
    cmp al, KEY_RSHIFT
    je .shift_pressed
    cmp al, KEY_CAPS
    je .caps_pressed

    ; Convertir le scancode en caractere
    call kb_scancode_to_char
    test al, al
    jz .end                     ; Caractere non mappable

    ; Ajouter le caractere au buffer
    call kb_buffer_put

.end:
    ; Acquitter l'interruption aupres du PIC
    mov al, 0x20
    out PIC1_CMD, al

    pop ds
    pop si
    pop bx
    pop ax
    iret

.key_released:
    ; Verifier le relachement de Shift
    cmp al, KEY_LSHIFT_REL
    je .shift_released
    cmp al, KEY_RSHIFT_REL
    je .shift_released
    jmp .end

.shift_pressed:
    mov byte [kb_shift_state], 1
    jmp .end

.shift_released:
    mov byte [kb_shift_state], 0
    jmp .end

.caps_pressed:
    xor byte [kb_caps_state], 1 ; Basculer Caps Lock
    jmp .end

;======================================================================
; kb_scancode_to_char - Convertit un scancode en caractere ASCII
; Entree:  AL = scancode
; Sortie:  AL = caractere (0 si non mappable)
;======================================================================
kb_scancode_to_char:
    push bx
    push si

    ; Verifier limites du scancode
    cmp al, 0x53
    ja .not_mapped

    xor bx, bx
    mov si, keymap_normal
    mov bl, al

    ; Verifier l'etat de Shift
    cmp byte [kb_shift_state], 1
    je .use_shift

    ; Pas de shift - utiliser keymap_normal
    mov al, [si + bx]
    jmp .check_caps

.use_shift:
    mov si, keymap_shift
    mov al, [si + bx]

.check_caps:
    ; Caps Lock : inverser la casse des lettres
    cmp byte [kb_caps_state], 1
    jne .done
    cmp al, 'a'
    jb .done
    cmp al, 'z'
    ja .done
    ; Inverser la casse
    xor al, 0x20                ; 'a' ^ 0x20 = 'A'

.done:
    pop si
    pop bx
    ret

.not_mapped:
    xor al, al
    pop si
    pop bx
    ret

;======================================================================
; kb_buffer_put - Ajoute un caractere au buffer circulaire
; Entree:  AL = caractere
;======================================================================
kb_buffer_put:
    push ax
    push bx
    push si

    mov si, kb_buffer
    xor bx, bx
    mov bl, [kb_buffer_tail]
    mov [si + bx], al

    ; Avancer la queue
    inc byte [kb_buffer_tail]
    and byte [kb_buffer_tail], 0xFF

    ; Verifier debordement (tete = queue)
    mov bl, [kb_buffer_head]
    cmp [kb_buffer_tail], bl
    jne .done
    ; Perte de donnees - reculer la queue
    dec byte [kb_buffer_tail]
    and byte [kb_buffer_tail], 0xFF

.done:
    pop si
    pop bx
    pop ax
    ret

;======================================================================
; kb_getchar - Lit un caractere depuis le buffer (non bloquant)
; Sortie:  AL = caractere (ZF=1 si buffer vide)
;======================================================================
kb_getchar:
    push bx
    push si

    mov si, kb_buffer
    xor bx, bx
    mov bl, [kb_buffer_head]

    ; Verifier si buffer vide (tete == queue)
    cmp bl, [kb_buffer_tail]
    je .empty

    ; Lire le caractere
    mov al, [si + bx]
    inc byte [kb_buffer_head]   ; Avancer la tete
    and byte [kb_buffer_head], 0xFF

    pop si
    pop bx
    test al, al                 ; ZF = 0 (caractere disponible)
    ret

.empty:
    xor al, al
    pop si
    pop bx
    test al, al                 ; ZF = 1 (buffer vide)
    ret

;======================================================================
; kb_waitchar - Attend et lit un caractere (bloquant)
; Sortie:  AL = caractere
;======================================================================
kb_waitchar:
    sti                         ; Interruptions activees
.loop:
    call kb_getchar
    jz .loop
    cli
    ret

;======================================================================
; kb_flush - Vide le buffer clavier
;======================================================================
kb_flush:
    push ax
    mov byte [kb_buffer_head], 0
    mov byte [kb_buffer_tail], 0
    pop ax
    ret

;======================================================================
; kb_readline - Lit une ligne de texte depuis le clavier
; Entree:  BX = buffer de destination
;          CX = taille max
; Sortie:  AX = nombre de caracteres lus (sans le 0 terminal)
;          Buffer rempli avec la ligne terminee par 0
;======================================================================
kb_readline:
    push bx
    push cx
    push di
    push dx

    mov di, bx                  ; DI = buffer
    xor dx, dx                  ; DX = compteur

.loop:
    sti
    call kb_waitchar
    cli

    cmp al, KEY_ENTER
    je .enter
    cmp al, KEY_BACKSPACE
    je .backspace

    ; Caractere normal
    cmp dx, cx                  ; Verifier taille max
    jae .loop

    ; Afficher le caractere
    push ax
    mov bl, [screen_attribute]
    call screen_putchar
    pop ax

    ; Stocker dans le buffer
    mov [di], al
    inc di
    inc dx
    jmp .loop

.backspace:
    cmp dx, 0                   ; Buffer vide?
    je .loop
    dec di
    dec dx
    ; Effacer a l'ecran
    mov al, 0x08
    mov bl, [screen_attribute]
    call screen_putchar
    mov al, ' '
    call screen_putchar
    mov al, 0x08
    call screen_putchar
    jmp .loop

.enter:
    ; Terminer la chaine
    mov byte [di], 0
    call screen_newline

    mov ax, dx                  ; Retourner le nombre de caracteres

    pop dx
    pop di
    pop cx
    pop bx
    ret
