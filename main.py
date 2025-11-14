import os
import sys
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.interface.app import main
import flet as ft

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"❌ Erro ao iniciar a aplicação: {e}")
        sys.exit(1)
