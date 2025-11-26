"""
Componente de card para exibir dietas utilizadas na simulação
"""

import flet as ft
from typing import List
from src.entities.alimento import AlimentoItem


def obter_categoria_alimento(nome: str) -> str:
    """Obtém a categoria de um alimento"""
    categorias = {
        'proteinas': ['frango', 'ovo', 'peixe', 'carne', 'leite', 'queijo'],
        'carboidratos': ['arroz', 'batata', 'quinoa', 'aveia', 'pão'],
        'leguminosas': ['feijão', 'lentilha', 'grão'],
        'vegetais': ['brócolis', 'espinafre', 'cenoura'],
        'frutas': ['banana', 'maçã', 'laranja', 'abacate'],
        'gorduras': ['azeite', 'castanha', 'amendoim']
    }
    
    nome_lower = nome.lower()
    for categoria, alimentos in categorias.items():
        if any(alim in nome_lower for alim in alimentos):
            return categoria
    return 'outros'


def agrupar_alimentos_por_categoria(alimentos: List[AlimentoItem]) -> dict:
    """Agrupa alimentos por categoria"""
    categorias = {
        'proteinas': [],
        'carboidratos': [],
        'leguminosas': [],
        'vegetais': [],
        'frutas': [],
        'gorduras': [],
        'outros': []
    }
    
    for alimento in alimentos:
        categoria = obter_categoria_alimento(alimento.nome)
        categorias[categoria].append(alimento)
    
    # Remove categorias vazias
    return {k: v for k, v in categorias.items() if v}


def criar_dieta_card(dieta: dict, indice: int, semanas_utilizadas: List[int] = None, destaque: str = None) -> ft.Container:
   
    alimentos = dieta['alimentos']
    calorias = dieta['calorias']
    

    categorias = agrupar_alimentos_por_categoria(alimentos)
    

    config_categorias = {
        'proteinas': {'icone': ft.Icons.EGG, 'cor': ft.Colors.RED_400, 'titulo': 'Proteinas'},
        'carboidratos': {'icone': ft.Icons.BAKERY_DINING, 'cor': ft.Colors.AMBER_700, 'titulo': 'Carboidratos'},
        'leguminosas': {'icone': ft.Icons.GRASS, 'cor': ft.Colors.BROWN_400, 'titulo': 'Leguminosas'},
        'vegetais': {'icone': ft.Icons.ECO, 'cor': ft.Colors.GREEN_600, 'titulo': 'Vegetais'},
        'frutas': {'icone': ft.Icons.APPLE, 'cor': ft.Colors.PINK_300, 'titulo': 'Frutas'},
        'gorduras': {'icone': ft.Icons.WATER_DROP, 'cor': ft.Colors.ORANGE_600, 'titulo': 'Gorduras Saudaveis'},
        'outros': {'icone': ft.Icons.RESTAURANT, 'cor': ft.Colors.GREY_600, 'titulo': 'Outros'}
    }
    
  
    categoria_widgets = []
    for categoria, alimentos_cat in categorias.items():
        config = config_categorias.get(categoria, config_categorias['outros'])
        

        alimentos_texto = ft.Column(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.CIRCLE, size=6, color=config['cor']),
                    ft.Text(
                        alimento.nome,
                        size=13,
                        color=ft.Colors.GREY_800,
                    ),
                    ft.Text(
                        f"({alimento.calorias:.0f} kcal)",
                        size=11,
                        color=ft.Colors.GREY_600,
                        italic=True,
                    ),
                ], spacing=8, tight=True)
                for alimento in alimentos_cat
            ],
            spacing=4,
            tight=True,
        )
        

        categoria_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(config['icone'], size=18, color=config['cor']),
                    ft.Text(
                        config['titulo'],
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=config['cor'],
                    ),
                ], spacing=8, tight=True),
                ft.Container(height=5),
                alimentos_texto,
            ], spacing=5, tight=True),
            padding=12,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.border.all(1.5, config['cor']),
        )
        categoria_widgets.append(categoria_card)
    
    # Texto sobre semanas utilizadas
    if semanas_utilizadas and len(semanas_utilizadas) > 0:
        if len(semanas_utilizadas) == 1:
            semanas_texto = f"Utilizada na semana {semanas_utilizadas[0]}"
        else:
            semanas_formatadas = ", ".join(str(s) for s in sorted(semanas_utilizadas))
            semanas_texto = f"Utilizada nas semanas: {semanas_formatadas}"
    else:
        semanas_texto = "Dieta gerada durante a simulacao"
    
    # Card principal
    card = ft.Container(
        content=ft.Column([
            # Cabeçalho do card
            ft.Row([
                ft.Container(
                    content=ft.Text(
                        f"#{indice}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    bgcolor=ft.Colors.ORANGE_700,
                    padding=10,
                    border_radius=10,
                    width=55,
                    height=55,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                f"Dieta Variacao {indice}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ORANGE_900,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "MAIOR CALORIAS" if destaque == 'maior' else "MENOR CALORIAS",
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                bgcolor=ft.Colors.RED_700 if destaque == 'maior' else ft.Colors.GREEN_700,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=6,
                            ) if destaque else ft.Container(),
                        ], spacing=10, tight=True),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, size=16, color=ft.Colors.ORANGE_700),
                            ft.Text(
                                f"{calorias:.0f} kcal",
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.ORANGE_700,
                            ),
                        ], spacing=5, tight=True),
                        ft.Row([
                            ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=ft.Colors.BLUE_600),
                            ft.Text(
                                semanas_texto,
                                size=12,
                                color=ft.Colors.BLUE_700,
                                italic=True,
                            ),
                        ], spacing=5, tight=True),
                    ], spacing=3, tight=True),
                    expand=True,
                ),
            ], spacing=15, alignment=ft.MainAxisAlignment.START),
            
            ft.Divider(height=1, color=ft.Colors.ORANGE_300),
            
            # Grid de categorias
            ft.Column(
                controls=categoria_widgets,
                spacing=10,
            ),
            
        ], spacing=15),
        padding=20,
        bgcolor=ft.Colors.RED_50 if destaque == 'maior' else (ft.Colors.GREEN_50 if destaque == 'menor' else ft.Colors.ORANGE_50),
        border_radius=15,
        border=ft.border.all(
            3 if destaque else 2,
            ft.Colors.RED_600 if destaque == 'maior' else (ft.Colors.GREEN_600 if destaque == 'menor' else ft.Colors.ORANGE_300)
        ),
        width=950,
        shadow=ft.BoxShadow(
            spread_radius=3 if destaque else 2,
            blur_radius=12 if destaque else 8,
            color=ft.Colors.with_opacity(0.20 if destaque else 0.12, ft.Colors.BLACK),
            offset=ft.Offset(0, 3 if destaque else 2),
        ),
    )
    
    return card
