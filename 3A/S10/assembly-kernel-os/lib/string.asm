;==============================================================================
; Fichier:   string.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Fonctions de manipulation de chaines
;
; Fonctions:
;   strlen          - Longueur d'une chaine
;   strcmp          - Comparaison de chaines
;   strcpy          - Copie de chaine
;   strcat          - Concatene deux chaines
;   strchr          - Cherche un caractere dans une chaine
;   strtoupper      - Convertit une chaine en majuscules
;   strtolower      - Convertit une chaine en minuscules
;   itoa            - Convertit un entier en chaine
;   atoi            - Convertit une chaine en entier
;   memset          - Remplit une zone memoire
;   memcpy          - Copie une zone memoire
;==============================================================================

;======================================================================
; strlen - Calcule la longueur d'une chaine
; Entree:  SI = adresse de la chaine (terminee par 0)
; Sortie:  AX = longueur
;======================================================================
strlen:
    push si
    push di

    mov di, si
    xor al, al
    cld
.loop:
    scasb
    jne .loop
    ; DI pointe apres le 0 terminal
    dec di
    mov ax, di
    sub ax, si                  ; AX = longueur

    pop di
    pop si
    ret

;======================================================================
; strcmp - Compare deux chaines
; Entree:  SI = chaine 1, DI = chaine 2
; Sortie:  AX = 0 si egales, <0 si s1 < s2, >0 si s1 > s2
;======================================================================
strcmp:
    push si
    push di
    push bx

    cld
.loop:
    lodsb
    scasb
    jne .different
    test al, al
    jnz .loop

    ; Chaines egales
    xor ax, ax
    jmp .done

.different:
    ; Calculer la difference
    movzx ax, byte [si - 1]
    movzx bx, byte [di - 1]
    sub ax, bx

.done:
    pop bx
    pop di
    pop si
    ret

;======================================================================
; strcpy - Copie une chaine dans une autre
; Entree:  SI = source, DI = destination
; Sortie:  DI = destination
;======================================================================
strcpy:
    push ax
    push si
    push di

    cld
.loop:
    lodsb
    stosb
    test al, al
    jnz .loop

    pop di
    pop si
    pop ax
    ret

;======================================================================
; strcat - Concatene src a la fin de dst
; Entree:  SI = source, DI = destination
; Sortie:  DI = destination
;======================================================================
strcat:
    push ax
    push si
    push di

    ; Aller a la fin de la destination
    push di
    xor al, al
    mov cx, 0xFFFF
    cld
    repne scasb
    dec di

    ; Copier la source
    pop si
    xchg si, di
    call strcpy

    pop di
    pop si
    pop ax
    ret

;======================================================================
; strchr - Cherche un caractere dans une chaine
; Entree:  SI = chaine, AL = caractere
; Sortie:  DI = adresse du caractere (0 si non trouve)
;======================================================================
strchr:
    push si
    push ax

    cld
.loop:
    lodsb
    cmp al, byte [esp]          ; Comparer avec le caractere cherche
    je .found
    test al, al
    jnz .loop

    ; Non trouve
    xor di, di
    jmp .done

.found:
    lea di, [si - 1]

.done:
    pop ax
    pop si
    ret

;======================================================================
; strtoupper - Convertit une chaine en majuscules
; Entree:  SI = chaine
; Sortie:  SI = chaine modifiee
;======================================================================
strtoupper:
    push si
    push ax

    cld
.loop:
    lodsb
    test al, al
    jz .done
    cmp al, 'a'
    jb .next
    cmp al, 'z'
    ja .next
    sub al, 0x20                ; Convertir en majuscule
    mov [si - 1], al
.next:
    jmp .loop
.done:
    pop ax
    pop si
    ret

;======================================================================
; strtolower - Convertit une chaine en minuscules
; Entree:  SI = chaine
; Sortie:  SI = chaine modifiee
;======================================================================
strtolower:
    push si
    push ax

    cld
.loop:
    lodsb
    test al, al
    jz .done
    cmp al, 'A'
    jb .next
    cmp al, 'Z'
    ja .next
    add al, 0x20                ; Convertir en minuscule
    mov [si - 1], al
.next:
    jmp .loop
.done:
    pop ax
    pop si
    ret

;======================================================================
; itoa - Convertit un entier non signe en chaine (base 10)
; Entree:  AX = valeur, DI = buffer destination
; Sortie:  DI = fin de la chaine
;======================================================================
itoa:
    push ax
    push bx
    push cx
    push dx
    push di

    mov cx, 10                  ; Base 10
    xor bx, bx                  ; Compteur de chiffres
    push bx                     ; Marqueur de fin

.div_loop:
    xor dx, dx
    div cx                      ; AX = quotient, DX = reste
    add dl, '0'                 ; Convertir en ASCII
    push dx                     ; Sauvegarder le chiffre
    inc bx
    test ax, ax
    jnz .div_loop

    ; Depiler les chiffres et les ecrire
    mov cx, bx
.write_loop:
    pop dx
    mov [di], dl
    inc di
    loop .write_loop

    mov byte [di], 0            ; Terminateur nul

    pop di
    pop dx
    pop cx
    pop bx
    pop ax
    ret

;======================================================================
; itoh - Convertit un entier en chaine hexadecimal
; Entree:  AX = valeur, DI = buffer destination
; Sortie:  DI = fin de chaine
;======================================================================
itoh:
    push ax
    push bx
    push cx
    push dx
    push di

    mov cx, 4                   ; 4 chiffres hexa
    push cx
    mov bx, 16                  ; Base 16

.div_loop:
    xor dx, dx
    div bx                      ; AX = quotient, DX = reste
    cmp dl, 10
    jb .digit
    add dl, 'A' - 10
    jmp .push_digit
.digit:
    add dl, '0'
.push_digit:
    push dx
    loop .div_loop

    mov cx, 4
.write_loop:
    pop dx
    mov [di], dl
    inc di
    loop .write_loop

    mov byte [di], 0            ; Terminateur nul

    pop cx
    pop di
    pop dx
    pop cx
    pop bx
    pop ax
    ret

;======================================================================
; atoi - Convertit une chaine en entier
; Entree:  SI = chaine
; Sortie:  AX = valeur
;======================================================================
atoi:
    push si
    push bx
    push dx

    xor ax, ax
    xor bx, bx
    xor dx, dx

    cld
.loop:
    lodsb
    test al, al
    jz .done
    cmp al, '0'
    jb .done
    cmp al, '9'
    ja .done

    sub al, '0'
    push ax
    mov ax, bx
    mov bx, 10
    mul bx                      ; AX = result * 10
    pop bx
    add bx, ax                  ; BX = result * 10 + digit
    jmp .loop

.done:
    mov ax, bx

    pop dx
    pop bx
    pop si
    ret

;======================================================================
; memset - Remplit une zone memoire avec un octet
; Entree:  DI = destination, CX = taille, AL = valeur
; Sortie:  DI = destination
;======================================================================
memset:
    push di
    push cx

    cld
    rep stosb

    pop cx
    pop di
    ret

;======================================================================
; memcpy - Copie une zone memoire
; Entree:  SI = source, DI = destination, CX = taille
; Sortie:  DI = destination
;======================================================================
memcpy:
    push si
    push di
    push cx

    cld
    rep movsb

    pop cx
    pop di
    pop si
    ret
