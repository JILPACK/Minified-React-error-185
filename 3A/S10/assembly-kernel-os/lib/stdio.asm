;==============================================================================
; Fichier:   stdio.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Fonctions d'entrees-sorties standard
;
; Fonctions:
;   printf          - Affiche une chaine formatee (support %%)
;   print_hex       - Affiche un nombre en hexadecimal
;   print_dec       - Affiche un nombre en decimal
;   print_help      - Affiche une aide utilisateur
;   print_newlines  - Affiche N lignes vides
;   cursor_save     - Sauvegarde la position du curseur
;   cursor_restore  - Restaure la position du curseur
;==============================================================================

;======================================================================
; printf - Affiche une chaine avec formatage simple
; Entree:  SI = chaine (attributs integres)
;======================================================================
printf:
    push si
    call screen_puts_attr
    pop si
    ret

;======================================================================
; print_hex - Affiche AX en hexadecimal (4 chiffres)
; Entree:  AX = valeur, BL = attribut
;======================================================================
print_hex:
    push ax
    push di
    push si

    ; Buffer local pour la conversion
    push ax
    mov di, sp
    push di
    call itoh
    pop si
    mov bl, [screen_attribute]
    call screen_puts
    pop ax                      ; Nettoyer la pile

    pop si
    pop di
    pop ax
    ret

;======================================================================
; print_dec - Affiche AX en decimal
; Entree:  AX = valeur, BL = attribut
;======================================================================
print_dec:
    push ax
    push di
    push si

    push ax
    mov di, sp
    push di
    call itoa
    pop si
    mov bl, [screen_attribute]
    call screen_puts
    pop ax

    pop si
    pop di
    pop ax
    ret

;======================================================================
; print_help - Affiche l'aide du systeme
;======================================================================
print_help:
    push si

    mov si, help_title
    call screen_puts_attr
    call screen_newline
    mov si, help_help
    call screen_puts_attr
    call screen_newline
    mov si, help_cls
    call screen_puts_attr
    call screen_newline
    mov si, help_echo
    call screen_puts_attr
    call screen_newline
    mov si, help_time
    call screen_puts_attr
    call screen_newline
    mov si, help_ticks
    call screen_puts_attr
    call screen_newline
    mov si, help_color
    call screen_puts_attr
    call screen_newline
    mov si, help_beep
    call screen_puts_attr
    call screen_newline
    mov si, help_info
    call screen_puts_attr
    call screen_newline
    mov si, help_reset
    call screen_puts_attr
    call screen_newline
    mov si, help_mem
    call screen_puts_attr
    call screen_newline
    mov si, help_calc
    call screen_puts_attr
    call screen_newline
    mov si, help_demo
    call screen_puts_attr
    call screen_newline

    pop si
    ret

;======================================================================
; print_newlines - Affiche N lignes vides
; Entree:  CX = nombre de lignes
;======================================================================
print_newlines:
    push ax
    push cx

.loop:
    call screen_newline
    loop .loop

    pop cx
    pop ax
    ret

;======================================================================
; saved_cursor - Stockage pour la position du curseur
;======================================================================
saved_cursor_row    db 0
saved_cursor_col    db 0

;======================================================================
; cursor_save - Sauvegarde la position du curseur
;======================================================================
cursor_save:
    push dx
    call screen_get_cursor
    mov [saved_cursor_row], dh
    mov [saved_cursor_col], dl
    pop dx
    ret

;======================================================================
; cursor_restore - Restaure la position du curseur
;======================================================================
cursor_restore:
    push dx
    mov dh, [saved_cursor_row]
    mov dl, [saved_cursor_col]
    call screen_set_cursor
    pop dx
    ret

;======================================================================
; Donnees d'aide (chaine + attribut par ligne)
;======================================================================
help_title  db ATTR_YELLOW_ON_BLACK, 'Commandes disponibles:', 0
help_help   db ATTR_CYAN_ON_BLACK, '  help    - Affiche cette aide', 0
help_cls    db ATTR_CYAN_ON_BLACK, '  cls     - Efface l ecran', 0
help_echo   db ATTR_CYAN_ON_BLACK, '  echo    - Affiche un message', 0
help_time   db ATTR_CYAN_ON_BLACK, '  time    - Affiche le temps systeme', 0
help_ticks  db ATTR_CYAN_ON_BLACK, '  ticks   - Affiche les ticks du timer', 0
help_color  db ATTR_CYAN_ON_BLACK, '  color   - Change la couleur (ex: color 0F)', 0
help_beep   db ATTR_CYAN_ON_BLACK, '  beep    - Emet un bip', 0
help_info   db ATTR_CYAN_ON_BLACK, '  info    - Affiche les infos systeme', 0
help_reset  db ATTR_CYAN_ON_BLACK, '  reset   - Redemarre le systeme', 0
help_mem    db ATTR_CYAN_ON_BLACK, '  mem     - Affiche l etat de la memoire', 0
help_calc   db ATTR_CYAN_ON_BLACK, '  calc    - Calcule une expression simple (ex: calc 2+3)', 0
help_demo   db ATTR_CYAN_ON_BLACK, '  demo    - Lance une demonstration', 0
