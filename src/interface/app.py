"""
Aplicação Principal de Interface Gráfica usando Flet
Simulador de Evolução Corporal com Otimização Genética de Dieta
"""

import flet as ft
from typing import List

from src.entities.alimento import AlimentoItem
from src.interface.pages import (
    PaginaDadosPessoais,
    PaginaFichaTreino,
    PaginaResultados,
    PaginaInformacoes,
)


class AppSimulador:
    """Aplicação principal - gerencia as páginas"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.alimentos = self._criar_cardapio()
        
        # Instanciar páginas
        self.pagina_dados = PaginaDadosPessoais(
            callback_validacao=self._on_dados_validados,
            callback_avancar_aba=self._avancar_aba
        )
        self.pagina_treino = PaginaFichaTreino(callback_confirmacao=self._on_treino_confirmado)
        self.pagina_resultados = PaginaResultados()
        self.pagina_info = PaginaInformacoes()
        
        # Referência para o Tabs (será definida em build())
        self.tabs = None
        
    def build(self):
        """Constrói a interface principal"""
        
        # Construir todas as abas
        tab_dados = self.pagina_dados.build()
        tab_treino = self.pagina_treino.build()
        tab_resultados = self.pagina_resultados.build()
        tab_info = self.pagina_info.build()
        
        # Criar o componente Tabs e armazenar referência
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[tab_dados, tab_treino, tab_resultados, tab_info],
            expand=True,
        )
        
        # Container principal
        return ft.Column(
            controls=[
                ft.AppBar(
                    title=ft.Text("Simulador de Evolucao Corporal", size=20, weight="bold"),
                    center_title=True,
                    bgcolor=ft.Colors.BLUE_700,
                ),
                self.tabs,
            ],
            expand=True,
        )
    
    def _on_dados_validados(self, individuo, semanas):
        """Callback chamado quando dados são validados"""
        # Preparar página de resultados com os dados validados
        self.pagina_resultados.set_parametros_simulacao(
            individuo=individuo,
            alimentos=self.alimentos,
            ficha_treino=None,  # Será definido quando a ficha for confirmada
            semanas=int(semanas) if semanas else 36
        )
        self.page.update()
    
    def _avancar_aba(self, indice_aba: int):
        """Avança para a aba especificada"""
        if self.tabs:
            self.tabs.selected_index = indice_aba
            self.page.update()
    
    def _on_treino_confirmado(self, ficha_treino):
        """Callback chamado quando ficha de treino é confirmada"""
        # Atualizar página de resultados com a ficha de treino
        individuo = self.pagina_dados.get_individuo()
        semanas = self.pagina_dados.get_semanas()
        
        if individuo:
            # Atualizar peso na página de treino para cálculos corretos
            self.pagina_treino.set_peso_individuo(individuo.peso)
            
            self.pagina_resultados.set_parametros_simulacao(
                individuo=individuo,
                alimentos=self.alimentos,
                ficha_treino=ficha_treino,
                semanas=int(semanas) if semanas else 36
            )
        self.page.update()
    
    def _criar_cardapio(self) -> List[AlimentoItem]:
        """Cria a lista padrão de alimentos"""
        return [
            AlimentoItem("Frango Grelhado", 165, 100),
            AlimentoItem("Ovo", 155, 100),
            AlimentoItem("Peixe", 206, 100),
            AlimentoItem("Carne Magra", 213, 100),
            AlimentoItem("Arroz Integral", 130, 100),
            AlimentoItem("Batata Doce", 86, 100),
            AlimentoItem("Quinoa", 120, 100),
            AlimentoItem("Aveia", 389, 100),
            AlimentoItem("Feijão Preto", 77, 100),
            AlimentoItem("Lentilha", 116, 100),
            AlimentoItem("Grão de Bico", 164, 100),
            AlimentoItem("Brócolis", 55, 100),
            AlimentoItem("Espinafre", 23, 100),
            AlimentoItem("Cenoura", 41, 100),
            AlimentoItem("Banana", 89, 100),
            AlimentoItem("Maçã", 52, 100),
            AlimentoItem("Laranja", 47, 100),
            AlimentoItem("Abacate", 160, 100),
            AlimentoItem("Azeite", 884, 100),
            AlimentoItem("Castanha", 553, 100),
            AlimentoItem("Amendoim", 567, 100),
            AlimentoItem("Leite Desnatado", 42, 100),
            AlimentoItem("Iogurte", 59, 100),
            AlimentoItem("Queijo Branco", 264, 100),
        ]


def main(page: ft.Page):
    """Função principal da aplicação"""
    page.title = "Simulador de Evolução Corporal"
    page.window_width = 1000
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    
    app = AppSimulador(page)
    page.add(app.build())


if __name__ == "__main__":
    ft.app(target=main)
