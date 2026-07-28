;==============================================================================
; Fichier:   kernel.inc
; Projet:    Assembly Kernel OS - 3AS10
; Auteur:    ENSEM NRJ (FISA)
; Description: Constantes, macros et structures pour le noyau
;==============================================================================

;--------- Adresses memoire ---------
%define KERNEL_BASE      0x1000      ; Adresse de chargement du noyau
%define KERNEL_SEGMENT   0x1000      ; Segment du noyau (0x1000 << 4 = 0x10000)
%define STACK_BASE       0x9000      ; Base de la pile
%define STACK_SIZE       0x1000      ; Taille de la pile
%define SCREEN_BASE      0xB8000     ; Memoire video VGA texte
%define SCREEN_SEGMENT   0xB800      ; Segment video

;--------- Dimensions ecran VGA -----
%define VGA_WIDTH        80          ; Colonnes
%define VGA_HEIGHT       25          ; Lignes
%define VGA_SIZE         2000        ; 80*25 mots
%define VGA_BYTES        4000        ; 80*25*2 octets

;--------- Couleurs VGA ------------
%define COLOR_BLACK      0x00
%define COLOR_BLUE       0x01
%define COLOR_GREEN      0x02
%define COLOR_CYAN       0x03
%define COLOR_RED        0x04
%define COLOR_MAGENTA    0x05
%define COLOR_BROWN      0x06
%define COLOR_LIGHT_GRAY 0x07
%define COLOR_DARK_GRAY  0x08
%define COLOR_LIGHT_BLUE 0x09
%define COLOR_LIGHT_GREEN 0x0A
%define COLOR_LIGHT_CYAN 0x0B
%define COLOR_LIGHT_RED  0x0C
%define COLOR_LIGHT_MAGENTA 0x0D
%define COLOR_YELLOW     0x0E
%define COLOR_WHITE      0x0F

; Attributs de couleur (background << 4 | foreground)
%define ATTR_WHITE_ON_BLACK   0x0F
%define ATTR_GREEN_ON_BLACK   0x02
%define ATTR_RED_ON_BLACK     0x04
%define ATTR_CYAN_ON_BLACK    0x03
%define ATTR_YELLOW_ON_BLACK  0x0E
%define ATTR_WHITE_ON_BLUE    0x1F
%define ATTR_WHITE_ON_RED     0x4F

;--------- Ports d'E/S ------------
%define KB_DATA_PORT      0x60      ; Port clavier (donnees)
%define KB_STATUS_PORT    0x64      ; Port clavier (statut)
%define KB_CMD_PORT       0x64      ; Port clavier (commande)
%define PIT_CH0           0x40      ; Timer canal 0
%define PIT_CMD           0x43      ; Timer commande
%define PIC1_CMD          0x20      ; PIC maitre commande
%define PIC1_DATA         0x21      ; PIC maitre donnees
%define PIC2_CMD          0xA0      ; PIC esclave commande
%define PIC2_DATA         0xA1      ; PIC esclave donnees

%define KEY_RELEASED      0x80      ; Masque touche relachee
%define KEY_ENTER         0x1C
%define KEY_BACKSPACE     0x0E
%define KEY_TAB           0x0F
%define KEY_LSHIFT        0x2A
%define KEY_RSHIFT        0x36
%define KEY_LSHIFT_REL    0xAA
%define KEY_RSHIFT_REL    0xB6
%define KEY_CAPS          0x3A
%define KEY_ESC           0x01
%define KEY_UP            0x48
%define KEY_DOWN          0x50
%define KEY_LEFT          0x4B
%define KEY_RIGHT         0x4D

;--------- Interruptions ------------
%define IRQ0_TIMER        0x20      ; Timer
%define IRQ1_KEYBOARD     0x21      ; Clavier

;--------- Systeme ----------------
%define CMD_BUFFER_SIZE   256       ; Taille buffer commandes
%define MAX_CMD_ARGS      16        ; Max arguments par commande
%define MAX_FILES         32        ; Max fichiers ouverts
%define HEAP_START        0x2000    ; Debut du tas
%define HEAP_SIZE         0x6000    ; Taille du tas (24 KB)

;--------- Macros assembleur --------
%macro outb 2
    mov al, %2
    out %1, al
%endmacro

%macro inb 1
    xor ah, ah
    in al, %1
%endmacro

%macro print_char 2
    push ax
    push bx
    mov al, %1
    mov bl, %2
    call screen_putchar
    pop bx
    pop ax
%endmacro

%macro print_string 2
    push ax
    push bx
    mov si, %1
    mov bl, %2
    call screen_puts
    pop bx
    pop ax
%endmacro

%macro set_cursor 2
    push ax
    mov dh, %1
    mov dl, %2
    call screen_set_cursor
    pop ax
%endmacro

%macro disable_interrupts 0
    pushf
    cli
%endmacro

%macro enable_interrupts 0
    popf
%endmacro
