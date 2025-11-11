#!/usr/bin/env python3
"""
Script para executar a interface gráfica Flet da Simulação de Evolução Corporal

Execução:
    python executar_interface.py
"""

import os
import sys

# Adicionar o diretório raiz ao path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.interface.app import main
import flet as ft

if __name__ == "__main__":
    print("🚀 Iniciando Interface de Simulação de Evolução Corporal...")
    print("📊 Interface baseada em Flet (Flutter for Python)")
    
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"❌ Erro ao iniciar a aplicação: {e}")
        sys.exit(1)
