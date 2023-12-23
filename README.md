## Introduction

這是 112-1 系統程式期末專題製作的 SIC/XE 組譯器

## How to run the assembler

若要執行程式，請依照以下格式輸入

python3 assembler.py <.asm file>

## Notice

此組譯器執行環境須為 Linux，並使用 python3，請確認環境皆符合要求再執行程式

因為目前只製作 PASS1，所以會將結果，也就是 OPTAB 和 SYMTAB 顯示於螢幕上，至於結果會寫在 objCode.txt 中，而目前開發只能成功寫入 H record 和 E record 而已
