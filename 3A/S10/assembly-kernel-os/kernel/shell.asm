;==============================================================================
; Fichier:   shell.asm
; Projet:    Assembly Kernel OS - 3AS10
; Description: Shell interactif - interface utilisateur du noyau
;
; Commandes implementees :
;   help    - Affiche l'aide
;   cls     - Efface l'ecran
;   echo    - Affiche un message
;   time    - Affiche le temps ecoule
;   ticks   - Affiche les ticks du timer
;   color   - Change la couleur du texte
;   beep    - Emet un bip sonore
;   info    - Affiche les informations systeme
;   reset   - Redemarre le systeme
;   mem     - Affiche l'etat de la memoire
;   calc    - Calcule une expression
;   demo    - Lance une demonstration
;==============================================================================

;--------- Variables du shell ---------
shell_prompt        db ATTR_GREEN_ON_BLACK, 'AOS> ', 0
shell_cmd_buffer    times CMD_BUFFER_SIZE db 0
shell_args          times MAX_CMD_ARGS * 2 db 0  ; Pointeurs d'arguments

;======================================================================
; shell_start - Point d'entree du shell
;======================================================================
shell_start:
    push ax
    push bx
    push cx
    push si
    push di

.main_loop:
    ; Afficher le prompt
    call cursor_save
    mov si, shell_prompt
    call screen_puts_attr

    ; Lire une ligne de commande
    mov bx, shell_cmd_buffer
    mov cx, CMD_BUFFER_SIZE - 1
    call kb_readline

    ; Analyser et executer la commande
    call shell_parse_and_exec

    jmp .main_loop

    pop di
    pop si
    pop cx
    pop bx
    pop ax
    ret

;======================================================================
; shell_parse_and_exec - Analyse et execute une commande
;======================================================================
shell_parse_and_exec:
    push si
    push di
    push ax
    push bx
    push cx

    ; Verifier si la ligne est vide
    mov si, shell_cmd_buffer
    lodsb
    test al, al
    jz .done                    ; Ligne vide

    ; Parse: separer la commande et les arguments
    mov si, shell_cmd_buffer
    call string_trim
    call string_tokenize

    ; La commande est dans shell_args[0]
    mov si, [shell_args]
    test si, si
    jz .done

    ; Convertir la commande en minuscules (insensible a la casse)
    push si
    call strtolower
    pop si

    ; Chercher et executer la commande
    call shell_dispatch

.done:
    pop cx
    pop bx
    pop ax
    pop di
    pop si
    ret

;======================================================================
; shell_dispatch - Aiguille la commande vers le bon handler
; Entree:  SI = commande
;======================================================================
shell_dispatch:
    push si
    push di
    push ax

    ; help
    mov di, cmd_help
    call strcmp
    test ax, ax
    jz .cmd_help

    ; cls
    mov di, cmd_cls
    call strcmp
    test ax, ax
    jz .cmd_cls

    ; echo
    mov di, cmd_echo
    call strcmp
    test ax, ax
    jz .cmd_echo

    ; time
    mov di, cmd_time
    call strcmp
    test ax, ax
    jz .cmd_time

    ; ticks
    mov di, cmd_ticks
    call strcmp
    test ax, ax
    jz .cmd_ticks

    ; color
    mov di, cmd_color
    call strcmp
    test ax, ax
    jz .cmd_color

    ; beep
    mov di, cmd_beep
    call strcmp
    test ax, ax
    jz .cmd_beep

    ; info
    mov di, cmd_info
    call strcmp
    test ax, ax
    jz .cmd_info

    ; reset
    mov di, cmd_reset
    call strcmp
    test ax, ax
    jz .cmd_reset

    ; mem
    mov di, cmd_mem
    call strcmp
    test ax, ax
    jz .cmd_mem

    ; calc
    mov di, cmd_calc
    call strcmp
    test ax, ax
    jz .cmd_calc

    ; demo
    mov di, cmd_demo
    call strcmp
    test ax, ax
    jz .cmd_demo

    ; Commande inconnue
    mov si, msg_unknown_cmd
    call screen_puts_attr
    call screen_newline
    jmp .done

.cmd_help:
    call cmd_handler_help
    jmp .done
.cmd_cls:
    call cmd_handler_cls
    jmp .done
.cmd_echo:
    call cmd_handler_echo
    jmp .done
.cmd_time:
    call cmd_handler_time
    jmp .done
.cmd_ticks:
    call cmd_handler_ticks
    jmp .done
.cmd_color:
    call cmd_handler_color
    jmp .done
.cmd_beep:
    call cmd_handler_beep
    jmp .done
.cmd_info:
    call cmd_handler_info
    jmp .done
.cmd_reset:
    call cmd_handler_reset
    jmp .done
.cmd_mem:
    call cmd_handler_mem
    jmp .done
.cmd_calc:
    call cmd_handler_calc
    jmp .done
.cmd_demo:
    call cmd_handler_demo
    jmp .done

.done:
    pop ax
    pop di
    pop si
    ret

;======================================================================
; string_trim - Supprime les espaces au debut et a la fin
; Entree:  SI = chaine
; Sortie:  SI = chaine trimmee (sur place)
;======================================================================
string_trim:
    push si
    push di
    push ax

    ; Supprimer les espaces au debut
    cld
.ltrim:
    lodsb
    cmp al, ' '
    je .ltrim
    cmp al, 0x09                ; Tab
    je .ltrim
    dec si                      ; Reculer sur le caractere non-espace

    ; Decaler la chaine vers le debut
    push si
    pop di
    mov si, di
    jmp .copy

.copy:
    lodsb
    stosb
    test al, al
    jnz .copy

    ; Supprimer les espaces a la fin
    dec di                      ; Reculer sur le 0
.rtrim:
    dec di
    cmp di, [esp]               ; Verifier si on revient au debut
    jb .done_rtrim
    mov al, [di]
    cmp al, ' '
    je .rtrim
    cmp al, 0x09
    je .rtrim
    inc di
.done_rtrim:
    mov byte [di], 0

    pop ax
    pop di
    pop si
    ret

;======================================================================
; string_tokenize - Decoupe la commande en arguments
; Entree:  SI = chaine
; Sortie:  shell_args = tableau de pointeurs termines par 0
;======================================================================
string_tokenize:
    push si
    push di
    push ax
    push cx

    mov di, shell_args
    xor cx, cx                  ; Compteur d'arguments

.skip_spaces:
    lodsb
    cmp al, ' '
    je .skip_spaces
    cmp al, 0x09
    je .skip_spaces
    test al, al
    jz .done

    ; Debut d'un argument
    dec si
    mov [di], si                ; Sauvegarder le pointeur
    add di, 2
    inc cx

    ; Chercher la fin de l'argument
.find_end:
    lodsb
    test al, al
    jz .done
    cmp al, ' '
    je .end_arg
    cmp al, 0x09
    je .end_arg
    jmp .find_end

.end_arg:
    dec si                      ; Reculer sur le separateur
    mov byte [si], 0            ; Terminer l'argument
    inc si                      ; Avancer apres le 0
    jmp .skip_spaces

.done:
    ; Terminer le tableau d'arguments
    xor ax, ax
    mov [di], ax

    pop cx
    pop ax
    pop di
    pop si
    ret

;======================================================================
; Gestionnaires de commandes
;======================================================================

;----- help -----
cmd_handler_help:
    call print_help
    ret

;----- cls -----
cmd_handler_cls:
    call screen_clear
    ret

;----- echo -----
cmd_handler_echo:
    push si
    mov si, [shell_args + 2]    ; Premier argument
    test si, si
    jz .done
    mov bl, [screen_attribute]
    call screen_puts
    call screen_newline
.done:
    pop si
    ret

;----- time -----
cmd_handler_time:
    push ax
    push si

    call isr_get_seconds
    mov si, msg_time_prefix
    call screen_puts_attr
    mov bl, [screen_attribute]
    call print_dec
    mov si, msg_time_suffix
    call screen_puts_attr
    call screen_newline

    pop si
    pop ax
    ret

;----- ticks -----
cmd_handler_ticks:
    push ax
    push si

    call isr_get_ticks
    mov si, msg_ticks_prefix
    call screen_puts_attr
    mov bl, [screen_attribute]
    call print_dec
    mov si, msg_ticks_suffix
    call screen_puts_attr
    call screen_newline

    pop si
    pop ax
    ret

;----- color -----
cmd_handler_color:
    push ax
    push bx
    push si

    mov si, [shell_args + 2]    ; Argument: code couleur hexa
    test si, si
    jz .show_current

    ; Convertir le code hexa
    call atoi
    test ax, ax
    jz .error
    cmp ax, 0xFF
    ja .error

    mov [screen_attribute], al
    mov si, msg_color_set
    call screen_puts_attr
    call screen_newline
    jmp .done

.show_current:
    mov si, msg_color_current
    call screen_puts_attr
    mov al, [screen_attribute]
    xor ah, ah
    mov bl, ATTR_WHITE_ON_BLACK
    call print_hex
    call screen_newline
    jmp .done

.error:
    mov si, msg_color_error
    call screen_puts_attr
    call screen_newline

.done:
    pop si
    pop bx
    pop ax
    ret

;----- beep -----
cmd_handler_beep:
    push ax
    push bx
    push cx

    ; Activer le PWM du PC speaker (PIT canal 2)
    mov al, 0xB6                ; Canal 2, mode 3, 16-bit
    out PIT_CMD, al
    call pic_io_delay

    ; Frequence ~440 Hz (La)
    mov ax, 2712                ; 1193180 / 440 = ~2712
    out 0x42, al
    call pic_io_delay
    mov al, ah
    out 0x42, al
    call pic_io_delay

    ; Activer le haut-parleur
    in al, 0x61
    or al, 0x03                 ; Bits 0 et 1
    out 0x61, al

    ; Attendre ~200 ms
    mov ax, 20
    call sleep

    ; Desactiver le haut-parleur
    in al, 0x61
    and al, 0xFC                ; Bits 0 et 1 a 0
    out 0x61, al

    pop cx
    pop bx
    pop ax
    ret

;----- info -----
cmd_handler_info:
    push si

    mov si, msg_info
    call screen_puts_attr
    call screen_newline

    ; Afficher les infos detaillees
    call display_sysinfo

    pop si
    ret

;----- reset -----
cmd_handler_reset:
    push si

    mov si, msg_reset_confirm
    call screen_puts_attr

    ; Attendre une touche
    call kb_waitchar

    ; Redemarrage via le BIOS
    mov si, msg_reset
    call screen_puts_attr
    call screen_newline

    ; Methode 1: Jumper vers le reset vector
    cli
    mov ax, 0xFFFF
    push ax
    mov ax, 0x0000
    push ax
    retf                        ; Saut far a 0xFFFF:0x0000

    pop si
    ret

;----- mem -----
cmd_handler_mem:
    push si
    push ax

    mov si, msg_mem_header
    call screen_puts_attr
    call screen_newline

    ; Afficher les regions memoire connues
    mov si, msg_mem_boot
    call screen_puts_attr
    call screen_newline

    mov si, msg_mem_kernel
    call screen_puts_attr
    call screen_newline

    mov si, msg_mem_stack
    call screen_puts_attr
    call screen_newline

    mov si, msg_mem_video
    call screen_puts_attr
    call screen_newline

    mov si, msg_mem_heap
    call screen_puts_attr
    call screen_newline

    pop ax
    pop si
    ret

;----- calc -----
cmd_handler_calc:
    push ax
    push bx
    push cx
    push si

    ; Recuperer l'expression
    mov si, [shell_args + 2]    ; Premier argument
    test si, si
    jz .error

    ; Analyser l'expression: nombre1 [+-] nombre2
    call parse_expression
    jc .error

    ; Afficher le resultat
    push si
    mov si, msg_calc_result
    call screen_puts_attr
    ; Afficher l'operande 1
    push ax
    mov ax, bx
    mov bl, [screen_attribute]
    call print_dec
    mov si, msg_calc_op
    call screen_puts_attr
    pop ax
    ; Afficher l'operande 2 et le resultat
    push ax
    mov ax, cx
    mov bl, [screen_attribute]
    call print_dec
    mov si, msg_calc_eq
    call screen_puts_attr
    pop ax
    mov ax, dx
    mov bl, [screen_attribute]
    call print_dec
    call screen_newline
    pop si
    jmp .done

.error:
    mov si, msg_calc_error
    call screen_puts_attr
    call screen_newline

.done:
    pop si
    pop cx
    pop bx
    pop ax
    ret

;----- demo -----
cmd_handler_demo:
    push ax
    push bx
    push cx
    push si
    push di

    mov si, msg_demo_start
    call screen_puts_attr
    call screen_newline

    ; Animation: barre de progression
    mov dh, [screen_cursor_row]
    inc dh
    mov dl, 0
    call screen_set_cursor

    mov cx, 40                  ; 40 etapes
    mov bl, ATTR_GREEN_ON_BLACK

.demo_loop:
    push cx
    push dx

    ; Afficher un bloc
    mov al, 0xDB                ; Bloc plein
    call screen_putchar

    ; Petit delai
    mov ax, 5
    call sleep

    pop dx
    pop cx
    loop .demo_loop

    call screen_newline
    mov si, msg_demo_done
    call screen_puts_attr
    call screen_newline

    pop di
    pop si
    pop cx
    pop bx
    pop ax
    ret

;======================================================================
; parse_expression - Analyse une expression mathematique simple
; Entree:  SI = chaine de l'expression (ex: "5+3")
; Sortie:  BX = operande 1, CX = operande 2, DX = resultat
;          CF = 0 si succes, 1 si erreur
;======================================================================
parse_expression:
    push si
    push ax
    push di

    ; Lire le premier nombre
    call atoi
    mov bx, ax                  ; BX = operande 1

    ; Chercher l'operateur
.scan_op:
    lodsb
    test al, al
    jz .error
    cmp al, '+'
    je .add
    cmp al, '-'
    je .sub
    cmp al, '*'
    je .mul
    cmp al, '/'
    je .div
    cmp al, ' '
    je .scan_op
    jmp .error

.add:
.skip_spaces_add:
    lodsb
    cmp al, ' '
    je .skip_spaces_add
    dec si
    call atoi
    mov cx, ax
    mov dx, bx
    add dx, cx                  ; DX = resultat
    clc
    jmp .done

.sub:
.skip_spaces_sub:
    lodsb
    cmp al, ' '
    je .skip_spaces_sub
    dec si
    call atoi
    mov cx, ax
    mov dx, bx
    sub dx, cx
    clc
    jmp .done

.mul:
.skip_spaces_mul:
    lodsb
    cmp al, ' '
    je .skip_spaces_mul
    dec si
    call atoi
    mov cx, ax
    mov ax, bx
    xor dx, dx
    mul cx
    mov dx, ax
    clc
    jmp .done

.div:
.skip_spaces_div:
    lodsb
    cmp al, ' '
    je .skip_spaces_div
    dec si
    call atoi
    mov cx, ax
    test cx, cx
    jz .error
    mov ax, bx
    xor dx, dx
    div cx
    mov dx, ax
    clc
    jmp .done

.error:
    stc

.done:
    pop di
    pop ax
    pop si
    ret

;======================================================================
; Commandes (chaines de reference)
;======================================================================
cmd_help    db 'help', 0
cmd_cls     db 'cls', 0
cmd_echo    db 'echo', 0
cmd_time    db 'time', 0
cmd_ticks   db 'ticks', 0
cmd_color   db 'color', 0
cmd_beep    db 'beep', 0
cmd_info    db 'info', 0
cmd_reset   db 'reset', 0
cmd_mem     db 'mem', 0
cmd_calc    db 'calc', 0
cmd_demo    db 'demo', 0

;======================================================================
; Messages du shell
;======================================================================
msg_unknown_cmd     db ATTR_RED_ON_BLACK, 'Commande inconnue. Tapez help pour l aide.', 0
msg_time_prefix     db ATTR_YELLOW_ON_BLACK, 'Temps systeme: ', 0
msg_time_suffix     db ATTR_YELLOW_ON_BLACK, ' secondes', 0
msg_ticks_prefix    db ATTR_YELLOW_ON_BLACK, 'Ticks timer: ', 0
msg_ticks_suffix    db ATTR_YELLOW_ON_BLACK, ' ticks', 0
msg_color_set       db ATTR_GREEN_ON_BLACK, 'Couleur changee.', 0
msg_color_current   db ATTR_YELLOW_ON_BLACK, 'Couleur actuelle: ', 0
msg_color_error     db ATTR_RED_ON_BLACK, 'Format: color <code_hexa> (ex: color 0F)', 0
msg_reset           db ATTR_RED_ON_BLACK, 'Redemarrage...', 0
msg_reset_confirm   db ATTR_YELLOW_ON_BLACK, 'Appuyez sur une touche pour confirmer le redemarrage...', 0
msg_info            db ATTR_CYAN_ON_BLACK, '=== Informations Systeme ===', 0
msg_mem_header      db ATTR_CYAN_ON_BLACK, '=== Etat de la Memoire ===', 0
msg_mem_boot        db ATTR_WHITE_ON_BLACK, '  Boot sector: 0x7C00 - 0x7DFF (512 o)', 0
msg_mem_kernel      db ATTR_WHITE_ON_BLACK, '  Noyau:       0x10000 - 0x17FFF (32 Ko)', 0
msg_mem_stack       db ATTR_WHITE_ON_BLACK, '  Pile:        0x9000 - 0x9FFF (4 Ko)', 0
msg_mem_video       db ATTR_WHITE_ON_BLACK, '  Video VGA:   0xB8000 - 0xB8F9F (4 Ko)', 0
msg_mem_heap        db ATTR_WHITE_ON_BLACK, '  Tas:         0x2000 - 0x7FFF (24 Ko)', 0
msg_calc_result     db ATTR_YELLOW_ON_BLACK, 'Resultat: ', 0
msg_calc_op         db ATTR_WHITE_ON_BLACK, ' ', 0
msg_calc_eq         db ATTR_WHITE_ON_BLACK, ' = ', 0
msg_calc_error      db ATTR_RED_ON_BLACK, 'Erreur de calcul. Format: calc <a>+<b>', 0
msg_demo_start      db ATTR_CYAN_ON_BLACK, '=== Demonstration - Barre de progression ===', 0
msg_demo_done       db ATTR_GREEN_ON_BLACK, 'Demonstration terminee!', 0
