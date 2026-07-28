;==============================================================================
; Fichier:   screen.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Pilote d'affichage VGA en mode texte 80x25
;
; Fonctions:
;   screen_init           - Initialise le mode texte
;   screen_clear          - Efface l'ecran
;   screen_putchar        - Affiche un caractere a la position courante
;   screen_puts           - Affiche une chaine sans attributs
;   screen_puts_attr      - Affiche une chaine avec attributs (format: attr,char,attr,char...)
;   screen_newline        - Passe a la ligne suivante
;   screen_scroll         - Fait defiler l'ecran
;   screen_set_cursor     - Positionne le curseur
;   screen_get_cursor     - Lit la position du curseur
;   screen_set_attribute  - Change l'attribut courant
;==============================================================================

;--------- Variables du pilote d'ecran ---------
screen_cursor_row   db 0        ; Ligne courante (0-24)
screen_cursor_col   db 0        ; Colonne courante (0-79)
screen_attribute    db ATTR_WHITE_ON_BLACK  ; Attribut courant

;======================================================================
; screen_init - Initialise le mode texte 80x25
;======================================================================
screen_init:
    push ax
    push bx
    push cx

    ; Mode texte 80x25 via BIOS
    mov ax, 0x0003
    int 0x10

    ; Initialiser le curseur
    mov byte [screen_cursor_row], 0
    mov byte [screen_cursor_col], 0
    mov byte [screen_attribute], ATTR_WHITE_ON_BLACK

    ; Effacer l'ecran
    call screen_clear

    pop cx
    pop bx
    pop ax
    ret

;======================================================================
; screen_clear - Efface l'ecran avec l'attribut courant
;======================================================================
screen_clear:
    push ax
    push bx
    push cx
    push di
    push es

    mov ax, SCREEN_SEGMENT
    mov es, ax
    xor di, di

    mov ah, [screen_attribute]
    mov al, ' '
    mov cx, VGA_SIZE
    cld
    rep stosw                    ; Remplir toute la memoire video

    ; Reinitialiser le curseur
    mov byte [screen_cursor_row], 0
    mov byte [screen_cursor_col], 0
    call screen_update_cursor

    pop es
    pop di
    pop cx
    pop bx
    pop ax
    ret

;======================================================================
; screen_putchar - Affiche un caractere a la position courante
; Entree:  AL = caractere, BL = attribut
;======================================================================
screen_putchar:
    push ax
    push bx
    push cx
    push di
    push es

    ; Gestion des caracteres speciaux
    cmp al, 0x0A                ; LF (line feed)
    je .newline
    cmp al, 0x0D                ; CR (carriage return)
    je .carriage_return
    cmp al, 0x08                ; Backspace
    je .backspace
    cmp al, 0x09                ; Tabulation
    je .tab

    ; Caractere normal - affichage
    push ax
    call screen_get_cursor_pos
    shl di, 1                   ; Position * 2 (chaque caractere = 2 octets)
    mov ah, bl                  ; Attribut
    pop ax
    stosw                       ; Ecrire dans la memoire video

    ; Avancer le curseur
    call screen_cursor_advance

.done:
    pop es
    pop di
    pop cx
    pop bx
    pop ax
    ret

.newline:
    mov byte [screen_cursor_col], 0
    inc byte [screen_cursor_row]
    call screen_check_scroll
    call screen_update_cursor
    jmp .done

.carriage_return:
    mov byte [screen_cursor_col], 0
    call screen_update_cursor
    jmp .done

.backspace:
    cmp byte [screen_cursor_col], 0
    je .done
    dec byte [screen_cursor_col]
    ; Effacer le caractere
    call screen_get_cursor_pos
    shl di, 1
    mov al, ' '
    mov ah, [screen_attribute]
    stosw
    call screen_update_cursor
    jmp .done

.tab:
    ; Avancer a la prochaine tabulation (tous les 8 caracteres)
    mov al, [screen_cursor_col]
    and al, 0xF8                ; Aligner a 8
    add al, 8
    cmp al, VGA_WIDTH
    jb .tab_ok
    mov al, 0
    inc byte [screen_cursor_row]
.tab_ok:
    mov [screen_cursor_col], al
    call screen_check_scroll
    call screen_update_cursor
    jmp .done

;======================================================================
; screen_puts - Affiche une chaine terminee par 0
; Entree:  SI = adresse chaine, BL = attribut
;======================================================================
screen_puts:
    push ax
    push si

    cld
.loop:
    lodsb
    test al, al
    jz .done
    call screen_putchar
    jmp .loop
.done:
    pop si
    pop ax
    ret

;======================================================================
; screen_puts_attr - Affiche une chaine avec un attribut
; Format: attr_byte, string_chars..., 0
; Entree:  SI = adresse (1er octet = attribut, reste = chaine)
;======================================================================
screen_puts_attr:
    push ax
    push bx
    push si

    cld
    lodsb                       ; Lire l'attribut
    mov bl, al
.loop:
    lodsb                       ; Lire le caractere
    test al, al
    jz .done
    call screen_putchar
    jmp .loop
.done:
    pop si
    pop bx
    pop ax
    ret

;======================================================================
; screen_newline - Nouvelle ligne
;======================================================================
screen_newline:
    push ax
    mov al, 0x0A
    mov bl, [screen_attribute]
    call screen_putchar
    pop ax
    ret

;======================================================================
; screen_scroll - Fait defiler l'ecran d'une ligne
;======================================================================
screen_scroll:
    push ax
    push cx
    push di
    push si
    push es
    push ds

    ; Copier lignes 1-24 vers lignes 0-23
    mov ax, SCREEN_SEGMENT
    mov es, ax
    mov ds, ax
    mov si, VGA_WIDTH * 2       ; Ligne 1
    mov di, 0                   ; Ligne 0
    mov cx, VGA_WIDTH * 24      ; 24 lignes
    cld
    rep movsw

    ; Effacer la derniere ligne
    mov di, VGA_WIDTH * 24 * 2  ; Debut ligne 24
    mov ah, [screen_attribute]
    mov al, ' '
    mov cx, VGA_WIDTH
    cld
    rep stosw

    pop ds
    pop es
    pop si
    pop di
    pop cx
    pop ax
    ret

;======================================================================
; screen_set_cursor - Positionne le curseur
; Entree:  DH = ligne, DL = colonne
;======================================================================
screen_set_cursor:
    push ax
    push dx

    mov [screen_cursor_row], dh
    mov [screen_cursor_col], dl
    call screen_update_cursor

    pop dx
    pop ax
    ret

;======================================================================
; screen_get_cursor - Lit la position du curseur
; Sortie:  DH = ligne, DL = colonne
;======================================================================
screen_get_cursor:
    mov dh, [screen_cursor_row]
    mov dl, [screen_cursor_col]
    ret

;======================================================================
; Fonctions internes
;======================================================================

; screen_get_cursor_pos - Convertit (row, col) en offset DI
screen_get_cursor_pos:
    push ax
    push bx
    mov al, [screen_cursor_row]
    mov bl, VGA_WIDTH
    mul bl                      ; AX = row * 80
    xor bh, bh
    mov bl, [screen_cursor_col]
    add ax, bx                  ; AX = row * 80 + col
    mov di, ax                  ; DI = offset
    pop bx
    pop ax
    ret

; screen_cursor_advance - Avance le curseur d'une position
screen_cursor_advance:
    push ax
    inc byte [screen_cursor_col]
    mov al, [screen_cursor_col]
    cmp al, VGA_WIDTH
    jb .done
    mov byte [screen_cursor_col], 0
    inc byte [screen_cursor_row]
    call screen_check_scroll
.done:
    call screen_update_cursor
    pop ax
    ret

; screen_check_scroll - Verifie si un defilement est necessaire
screen_check_scroll:
    push ax
    mov al, [screen_cursor_row]
    cmp al, VGA_HEIGHT
    jb .done
    mov byte [screen_cursor_row], VGA_HEIGHT - 1
    call screen_scroll
.done:
    pop ax
    ret

; screen_update_cursor - Met a jour le curseur materiel via BIOS
screen_update_cursor:
    push ax
    push bx
    push dx

    mov ah, 0x02                ; Fonction position curseur
    xor bh, bh                  ; Page 0
    mov dh, [screen_cursor_row] ; Ligne
    mov dl, [screen_cursor_col] ; Colonne
    int 0x10

    pop dx
    pop bx
    pop ax
    ret
