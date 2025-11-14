
import flet as ft
class PaginaInformacoes:
   

    def __init__(self):
        self.info_sections = [
            {
                "icon": ft.Icons.SCIENCE_OUTLINED,
                "title": "SOBRE A SIMULAÇÃO",
                "text": "Esta aplicação simula a evolução corporal de um indivíduo ao longo de semanas, considerando:",
                "list_items": [
                    "Cálculo do Gasto Calórico (Harris-Benedict)",
                    "Otimização Genética de Seleção de Alimentos",
                    "Diferentes Fichas de Treino (ABC, ABCD, PPL)",
                    "Mudanças de Composição Corporal",
                    "Ajustes Metabólicos Dinâmicos"
                ],
                "color": ft.Colors.BLUE_GREY_700
            },
            {
                "icon": ft.Icons.MENU_BOOK_OUTLINED,
                "title": "FONTES CIENTÍFICAS",
                "text": "A simulação é baseada nas seguintes publicações e padrões:",
                "list_items": [
                    "Harris-Benedict (1919) - Taxa Metabólica Basal",
                    "Compendium of Physical Activities (2024) - METs",
                    "Jackson & Pollock (1978) - Composição Corporal",
                    "WHO (1995) - Índice de Massa Corporal"
                ],
                "color": ft.Colors.BLUE_GREY_700
            },
            {
                "icon": ft.Icons.BUILD_OUTLINED,
                "title": "TECNOLOGIA",
                "text": "Componentes tecnológicos utilizados no desenvolvimento:",
                "list_items": [
                    "Flet - Interface Gráfica",
                    "Algoritmo Genético - Otimização de Dieta",
                    "Matplotlib - Visualização de Gráficos",
                    "Python 3.10+"
                ],
                "color": ft.Colors.BLUE_GREY_700
            },
            {
                "icon": ft.Icons.WARNING_AMBER_ROUNDED,
                "title": "AVISO IMPORTANTE",
                "text": "Esta é uma simulação educacional para fins acadêmicos. Não deve ser usada para prescrição nutricional ou médica.",
                "list_items": [],
                "color": ft.Colors.RED_700  
            },
            {
                "icon": ft.Icons.DESCRIPTION_OUTLINED,
                "title": "DOCUMENTAÇÃO",
                "text": "Para mais detalhes, consulte os arquivos de validação e fontes no repositório do projeto:",
                "list_items": [
                    "FONTES_CIENTIFICAS.md",
                    "VALIDACAO_FONTES.md"
                ],
                "color": ft.Colors.BLUE_GREY_700
            }
        ]

    def _create_info_card(self, section: dict) -> ft.Card:
   
        list_controls = []
        if section.get("list_items"):
            for item in section["list_items"]:
                list_controls.append(
                    ft.Row(
                        controls=[
                            ft.Icon(
                                
                                ft.Icons.CHECK_CIRCLE_OUTLINE if section["title"] != "DOCUMENTAÇÃO" 
                                else ft.Icons.ARTICLE_OUTLINED,
                                color=ft.Colors.GREEN_700 if section["title"] != "DOCUMENTAÇÃO" else ft.Colors.GREY_700,
                                size=18
                            ),
                            ft.Text(item, size=14, color=ft.Colors.BLACK87, expand=True), 
                        ],
                        spacing=10
                    )
                )

        return ft.Card(
            elevation=2.0,  
            content=ft.Container(
                content=ft.Column(
                    controls=[
                       
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
                        ft.Divider(height=1, color=ft.Colors.GREY_300),
                        
                      
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        section["text"],
                                        size=15,
                                        color=ft.Colors.BLACK87,
                                        italic=(section["title"] == "AVISO IMPORTANTE") 
                                    ),
                               
                                    ft.Column(list_controls, spacing=5) if list_controls else ft.Container()
                                ],
                                spacing=10
                            ),
                            padding=ft.padding.only(left=10, right=10, top=10, bottom=15)
                        )
                    ],
                    spacing=5 
                ),
                padding=10, 
                border_radius=ft.border_radius.all(8)
            )
        )

    def _build_content_view(self) -> ft.Container:
      
        info_cards = [self._create_info_card(section) for section in self.info_sections]
        
        return ft.Container(
           
            bgcolor=ft.Colors.GREY_100,
            padding=ft.padding.symmetric(horizontal=10, vertical=15),
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                controls=info_cards,
                scroll=ft.ScrollMode.AUTO, 
                spacing=15, 
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH 
            )
        )

    def build(self) -> ft.Tab:
        
        return ft.Tab(
            text="Informações",
            icon=ft.Icons.INFO_OUTLINE, 
            content=self._build_content_view()
        )

def main(page: ft.Page):
  
    page.title = "Teste da Página de Informações"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 500
    page.window_height = 800

 
    pagina_info = PaginaInformacoes()

    
    tabs_control = ft.Tabs(
        selected_index=0,
        expand=1,
        tabs=[
            pagina_info.build()  
        ]
    )
    
    page.appbar = ft.AppBar(
        title=ft.Text("Simulador de Evolução Corporal"),
        bgcolor=ft.Colors.BLUE_GREY_800
    )

    page.add(tabs_control)
    page.update()
