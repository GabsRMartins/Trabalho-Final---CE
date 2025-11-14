#!/usr/bin/env python3
"""
Ponto de entrada (Entry Point) para a Simulação de Evolução Corporal.

Este script configura o ambiente (sys.path) e inicia a 
interface gráfica principal da aplicação Flet.

Execução:
    python executar_interface.py
"""

# --- 1. Importações da Biblioteca Padrão ---
import os
import sys

# --- 2. Configuração do Path do Projeto ---
# Adiciona o diretório raiz ao sys.path para garantir que 
# os módulos em 'src' possam ser encontrados e importados.
try:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
except NameError:
    # Fallback caso __file__ não esteja definido (ex: em alguns REPLs)
    print("Aviso: __file__ não definido. Assumindo diretório atual como raiz.")
    sys.path.insert(0, os.getcwd())


# --- 3. Importações de Terceiros e do Projeto ---
import flet as ft

try:
    # Importa a função 'main' de dentro do pacote da interface
    from src.interface.app import main as main_app
except ImportError as e:
    print(f"❌ Erro Fatal: Não foi possível encontrar o módulo 'src.interface.app'.")
    print(f"Certifique-se de que a estrutura de pastas (src/interface/app.py) está correta.")
    print(f"Detalhe do erro: {e}")
    sys.exit(1) # Encerra o script se o módulo principal não for encontrado


# --- 4. Função de Execução Principal ---
def run_application():
    """
    Configura e inicia a aplicação Flet.
    """
    print("🚀 Iniciando Interface de Simulação de Evolução Corporal...")
    try:
        # Inicia a aplicação Flet passando a função 'main' importada
        ft.app(target=main_app)
        
    except Exception as e:
        # Captura qualquer erro inesperado durante a execução da app
        print(f"❌ Erro crítico ao executar a aplicação: {e}")
        sys.exit(1)

# --- 5. Ponto de Entrada Padrão ---
if __name__ == "__main__":
    # Chama a função de execução
    run_application()
