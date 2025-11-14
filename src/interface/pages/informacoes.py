"""
Módulo refatorado para a aba de Informações.

Esta versão melhora a estrutura, separando os dados da lógica da interface,
e utiliza Cards e Ícones para uma apresentação visual mais agradável.
"""

import flet as ft

class PaginaInformacoes:
    """
    Constrói a aba de "Informações" da aplicação, exibindo detalhes
    sobre o projeto, fontes e tecnologia em um layout de cartões.
    """

    def __init__(self):
        """
        Inicializa a página.
        Os dados de informação são carregados aqui para fácil manutenção.
        """
        # 1. DADOS ESTRUTURADOS
        # Manter os dados separados da UI facilita a atualização.
        # Cada dicionário representa um "Card" na interface.
        self.info_sections = [
            {
                "icon": ft.icons.SCIENCE_OUTLINED,
                "title": "SOBRE A SIMULAÇÃO",
                "text": "Esta aplicação simula a evolução corporal de um indivíduo ao longo de semanas, considerando:",
                "list_items": [
                    "Cálculo do Gasto Calórico (Harris-Benedict)",
                    "Otimização Genética de Seleção de Alimentos",
                    "Diferentes Fichas de Treino (ABC, ABCD, PPL)",
                    "Mudanças de Composição Corporal",
                    "Ajustes Metabólicos Dinâmicos"
                ],
                "color": ft.colors.BLUE_GREY_700
            },
            {
                "icon": ft.icons.MENU_BOOK_OUTLINED,
                "title": "FONTES CIENTÍFICAS",
                "text": "A simulação é baseada nas seguintes publicações e padrões:",
                "list_items": [
                    "Harris-Benedict (1919) - Taxa Metabólica Basal",
                    "Compendium of Physical Activities (2024) - METs",
                    "Jackson & Pollock (1978) - Composição Corporal",
                    "WHO (1995) - Índice de Massa Corporal"
                ],
                "color": ft.colors.BLUE_GREY_700
            },
            {
                "icon": ft.icons.BUILD_OUTLINED,
                "title": "TECNOLOGIA",
                "text": "Componentes tecnológicos utilizados no desenvolvimento:",
                "list_items": [
                    "Flet - Interface Gráfica",
                    "Algoritmo Genético - Otimização de Dieta",
                    "Matplotlib - Visualização de Gráficos",
                    "Python 3.10+"
                ],
                "color": ft.colors.BLUE_GREY_700
            },
            {
                "icon": ft.icons.WARNING_AMBER_ROUNDED,
                "title": "AVISO IMPORTANTE",
                "text": "Esta é uma simulação educacional para fins acadêmicos. Não deve ser usada para prescrição nutricional ou médica.",
                "list_items": [],
                "color": ft.colors.RED_700  # Cor de destaque para o aviso
            },
            {
                "icon": ft.icons.DESCRIPTION_OUTLINED,
                "title": "DOCUMENTAÇÃO",
                "text": "Para mais detalhes, consulte os arquivos de validação e fontes no repositório do projeto:",
                "list_items": [
                    "FONTES_CIENTIFICAS.md",
                    "VALIDACAO_FONTES.md"
                ],
                "color": ft.colors.BLUE_GREY_700
            }
        ]

    def _create_info_card(self, section: dict) -> ft.Card:
        """
        Cria um widget de Card individual para uma seção de informação.
        
        Args:
            section: Um dicionário contendo 'icon', 'title', 'text', 'list_items' e 'color'.

        Returns:
            Um ft.Card pronto para ser exibido.
        """
        
        # --- Constrói a lista de itens (se houver) ---
        list_controls = []
        if section.get("list_items"): # Verifica se a lista existe e não está vazia
            for item in section["list_items"]:
                list_controls.append(
                    ft.Row(
                        controls=[
                            ft.Icon(
                                # Usa ícones diferentes para itens de lista
                                ft.icons.CHECK_CIRCLE_OUTLINE if section["title"] != "DOCUMENTAÇÃO" 
                                else ft.icons.ARTICLE_OUTLINED,
                                color=ft.colors.GREEN_700 if section["title"] != "DOCUMENTAÇÃO" else ft.colors.GREY_700,
                                size=18
                            ),
                            ft.Text(item, size=14, color=ft.colors.BLACK87, expand=True), # expand=True garante a quebra de linha
                        ],
                        spacing=10
                    )
                )

        # --- Constrói o Card ---
        return ft.Card(
            elevation=2.0,  # Sombra leve
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # --- Linha do Título ---
                        ft.Row(
                            controls=[
                                ft.Icon(section["icon"], color=section["color"], size=24),
                                ft.Text(
                                    section["title"],
                                    style=ft.TextThemeStyle.TITLE_LARGE,
                                    weight=ft.FontWeight.BOLD,
                                    color=section["color"],
                                    size=18
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        ft.Divider(height=1, color=ft.colors.GREY_300),
                        
                        # --- Container do Conteúdo ---
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        section["text"],
                                        size=15,
                                        color=ft.colors.BLACK87,
                                        italic=(section["title"] == "AVISO IMPORTANTE") # Coloca aviso em itálico
                                    ),
                                    # Adiciona a coluna de lista de itens (se houver)
                                    ft.Column(list_controls, spacing=5) if list_controls else ft.Container()
                                ],
                                spacing=10
                            ),
                            padding=ft.padding.only(left=10, right=10, top=10, bottom=15)
                        )
                    ],
                    spacing=5 # Espaçamento interno do Card
                ),
                padding=10, # Padding geral do Card
                border_radius=ft.border_radius.all(8)
            )
        )

    def _build_content_view(self) -> ft.Container:
        """
        Constrói a visão principal da aba, iterando sobre os dados
        e criando os cards.
        """
        # 3. CONSTRUÇÃO DA VIEW
        # A lógica de UI apenas itera sobre os dados e chama o construtor de Card.
        info_cards = [self._create_info_card(section) for section in self.info_sections]
        
        return ft.Container(
            # Define uma cor de fundo sutil para a aba
            bgcolor=ft.colors.GREY_100,
            padding=ft.padding.symmetric(horizontal=10, vertical=15),
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                controls=info_cards,
                scroll=ft.ScrollMode.AUTO, # Habilita a rolagem
                spacing=15, # Espaço entre os cards
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH # Faz os cards ocuparem a largura
            )
        )

    def build(self) -> ft.Tab:
        """
        Ponto de entrada principal para construir o widget da aba.
        """
        # 2. PONTO DE ENTRADA (Build)
        # O método build agora é limpo e apenas monta a Tab.
        # O conteúdo real é delegado para _build_content_view.
        return ft.Tab(
            text="Informações",
            icon=ft.icons.INFO_OUTLINE, # Ícone na própria aba
            content=self._build_content_view()
        )

# --- Código de Exemplo para Testar a Página ---
def main(page: ft.Page):
    """
    Função principal para executar e testar esta página de forma independente.
    """
    page.title = "Teste da Página de Informações"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 500
    page.window_height = 800

    # Cria a instância da nossa página
    pagina_info = PaginaInformacoes()

    # Adiciona a um controle de Tabs para visualização
    tabs_control = ft.Tabs(
        selected_index=0,
        expand=1,
        tabs=[
            pagina_info.build()  # Chama o método build da nossa classe
            # Você poderia adicionar outras tabs aqui para teste
            # ft.Tab(text="Outra Aba", icon=ft.icons.HOME, content=ft.Text("Conteúdo da outra aba"))
        ]
    )
    
    page.appbar = ft.AppBar(
        title=ft.Text("Simulador de Evolução Corporal"),
        bgcolor=ft.colors.BLUE_GREY_800
    )

    page.add(tabs_control)
    page.update()

if __name__ == "__main__":
    # Executa o aplicativo Flet
    ft.app(target=main)
