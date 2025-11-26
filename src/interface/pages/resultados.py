"""
Módulo para aba de Resultados
"""

import flet as ft
import copy

from src.service.simulation import simular_evolucao
from src.entities.individuo import Individuo
from src.interface.util.graficos import criar_graficos_evolucao
from src.utils.alg_utils import obter_historico_dietas, resetar_cache_elitismo
from src.interface.components.dieta_card import criar_dieta_card


class PaginaResultados:

    def __init__(self):
        self.individuo_original = None
        self.alimentos = None
        self.ficha_treino = None
        self.semanas = 36
        self.btn_executar = None
        
    def build(self):
        
        self.alert_placeholder = ft.Column(controls=[], tight=True)
        
        self.txt_status = ft.Text(
            value="Configure os dados e escolha uma ficha de treino para iniciar",
            size=14,
            color=ft.Colors.BLUE_GREY_600,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
        )
        
        self.progress_bar = ft.ProgressBar(visible=False, color=ft.Colors.BLUE_700)
        
        self.container_resumo = ft.Row(spacing=15, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        self.container_graficos = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.container_dietas = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        

        self.resumo_wrapper = ft.Container(
            content=ft.Column([
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ASSESSMENT, size=26, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Resumo da Evolucao",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Container(height=15),
                self.container_resumo,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
        
        self.graficos_wrapper = ft.Container(
            content=ft.Column([
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SHOW_CHART, size=26, color=ft.Colors.GREEN_700),
                        ft.Text(
                            "Graficos de Evolucao",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Container(height=15),
                self.container_graficos,
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
        
        # Container wrapper para as dietas utilizadas
        self.dietas_wrapper = ft.Container(
            content=ft.Column([
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.RESTAURANT_MENU, size=26, color=ft.Colors.ORANGE_700),
                        ft.Text(
                            "Dietas Utilizadas na Simulacao",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Text(
                    "Mostrando ate 10 variacoes de dietas geradas pelo algoritmo genetico",
                    size=13,
                    color=ft.Colors.GREY_600,
                    italic=True,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=15),
                self.container_dietas,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
        

        self.btn_executar = ft.Container(
            content=ft.ElevatedButton(
                text="Executar Simulacao",
                icon=ft.Icons.PLAY_ARROW,
                on_click=self._executar_simulacao,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                height=55,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
            ),
            width=400,
        )
        

        self.content_column = ft.Container(
            content=ft.Column(
                controls=[

                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.ROCKET_LAUNCH, size=32, color=ft.Colors.BLUE_700),
                                ft.Text(
                                    "Simulacao de Evolucao",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_700,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12,
                        ),
                        margin=ft.margin.only(bottom=20),
                    ),
                    
                    self.alert_placeholder,
                    
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            self.txt_status,
                                            ft.Container(height=15),
                                            self.btn_executar,
                                            ft.Container(height=10),
                                            self.progress_bar,
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=30,
                                    bgcolor=ft.Colors.BLUE_50,
                                    border_radius=12,
                                    border=ft.border.all(2, ft.Colors.BLUE_200),
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=ft.Colors.WHITE,
                        padding=25,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                            offset=ft.Offset(0, 2),
                        ),
                        width=500,
                    ),
                    
                    ft.Container(height=30),
                    

                    self.resumo_wrapper,
                    ft.Container(height=20),
                    self.graficos_wrapper,
                    ft.Container(height=20),
                    self.dietas_wrapper,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=30,
            bgcolor=ft.Colors.GREY_50,
            expand=True,
        )
        
        return ft.Tab(
            text="Resultados",
            content=self.content_column,
        )
    
    def set_parametros_simulacao(self, individuo, alimentos, ficha_treino, semanas):
        self.individuo_original = individuo
        self.alimentos = alimentos
        self.ficha_treino = ficha_treino
        self.semanas = semanas
    
    def _executar_simulacao(self, e):
        if not self.individuo_original or not self.ficha_treino:
            from src.interface.components.alert import Alert
            alerta = Alert("Complete os dados e escolha uma ficha de treino!", alert_type="error", on_close=self._close_alert)
            self.alert_placeholder.controls = [alerta]
            self.alert_placeholder.update()
            return
        
        try:
            # Desabilitar botão
            self.btn_executar.disabled = True
            self.btn_executar.opacity = 0.5
            self.btn_executar.update()
            

            resetar_cache_elitismo()
            
            self.txt_status.value = "Executando simulacao... Por favor aguarde..."
            self.txt_status.color = ft.Colors.ORANGE_700
            self.progress_bar.visible = True
            self.txt_status.update()
            self.progress_bar.update()
            
            individuo_sim = copy.deepcopy(self.individuo_original)
            simular_evolucao(individuo_sim, self.alimentos, self.ficha_treino, self.semanas)
            
            self._exibir_resultados(individuo_sim)
            
            self.txt_status.value = "Simulacao Concluida com Sucesso!"
            self.txt_status.color = ft.Colors.GREEN_600
            self.progress_bar.visible = False
            self.txt_status.update()
            self.progress_bar.update()
            
            try:
                self.btn_executar.page.update()
            except:
                pass
            
        except Exception as ex:
            from src.interface.components.alert import Alert
            import traceback
            alerta = Alert(f"Erro: {str(ex)}", alert_type="error", on_close=self._close_alert)
            self.alert_placeholder.controls = [alerta]
            self.alert_placeholder.update()
            self.progress_bar.visible = False
            self.progress_bar.update()
            print(traceback.format_exc())
        
        finally:
            # Reabilitar botão
            self.btn_executar.disabled = False
            self.btn_executar.opacity = 1.0
            self.btn_executar.update()
    
    def _close_alert(self, e):
        self.alert_placeholder.controls = []
        try:
            self.alert_placeholder.update()
        except:
            pass
    
    def _exibir_resultados(self, individuo_sim: Individuo):
        """Exibe os resultados da simulação"""
        
        self.container_resumo.controls.clear()
        self.container_graficos.controls.clear()
        
        mudanca_peso = individuo_sim.peso - self.individuo_original.peso
        mudanca_imc = individuo_sim.calcular_imc() - self.individuo_original.calcular_imc()
        mudanca_gordura = individuo_sim.taxa_gordura - self.individuo_original.taxa_gordura
        
        massa_magra_inicial = self.individuo_original.peso * (100 - self.individuo_original.taxa_gordura) / 100
        massa_magra_final = individuo_sim.peso * (100 - individuo_sim.taxa_gordura) / 100
        mudanca_massa_magra = massa_magra_final - massa_magra_inicial
        
        # Cards de resumo
        card_peso = self._criar_card_resumo(
            titulo="Peso",
            valor_inicial=f"{self.individuo_original.peso:.1f} kg",
            valor_final=f"{individuo_sim.peso:.1f} kg",
            variacao=mudanca_peso,
            unidade="kg",
            cor=ft.Colors.BLUE_GREY_700
        )
        
        card_imc = self._criar_card_resumo(
            titulo="IMC",
            valor_inicial=f"{self.individuo_original.calcular_imc():.1f}",
            valor_final=f"{individuo_sim.calcular_imc():.1f}",
            variacao=mudanca_imc,
            unidade="",
            cor=ft.Colors.AMBER_600
        )
        
        card_gordura = self._criar_card_resumo(
            titulo="Taxa de Gordura",
            valor_inicial=f"{self.individuo_original.taxa_gordura:.1f}%",
            valor_final=f"{individuo_sim.taxa_gordura:.1f}%",
            variacao=mudanca_gordura,
            unidade="%",
            cor=ft.Colors.PINK_400
        )
        
        card_massa_magra = self._criar_card_resumo(
            titulo="Massa Magra",
            valor_inicial=f"{massa_magra_inicial:.1f} kg",
            valor_final=f"{massa_magra_final:.1f} kg",
            variacao=mudanca_massa_magra,
            unidade="kg",
            cor=ft.Colors.DEEP_PURPLE_500
        )
        
        self.container_resumo.controls.extend([card_peso, card_imc, card_gordura, card_massa_magra])
        
        self.resumo_wrapper.visible = True
        self.resumo_wrapper.update()

        try:
            image_base64 = criar_graficos_evolucao(self.individuo_original, individuo_sim)
            
            image_widget = ft.Image(
                src_base64=image_base64,
                width=1000,
                height=850,
                fit=ft.ImageFit.CONTAIN,
            )
            
            self.container_graficos.controls.append(
                ft.Container(
                    content=image_widget,
                    padding=10,
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=10,
                    width=1050,
                )
            )
            
            self.graficos_wrapper.visible = True
            self.graficos_wrapper.update()
            
        except Exception as ex:
            self.container_graficos.controls.append(
                ft.Text(
                    value=f"Erro ao gerar gráficos: {str(ex)}",
                    color=ft.Colors.RED,
                    size=12,
                )
            )
            self.graficos_wrapper.visible = True
            self.graficos_wrapper.update()
        
        # Exibir histórico de dietas
        self._exibir_dietas()
    
    def _criar_card_resumo(self, titulo: str, valor_inicial: str, valor_final: str, variacao: float, unidade: str, cor: str) -> ft.Container:
   
        cor_variacao = ft.Colors.GREEN_600 if variacao >= 0 else ft.Colors.RED_600
        simbolo_variacao = "+" if variacao >= 0 else ""
        
        if titulo == "Taxa de Gordura" and variacao < 0:
            cor_variacao = ft.Colors.GREEN_600
            simbolo_variacao = ""
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    titulo,
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=8),

                ft.Column([
                    ft.Row([
                        ft.Text("Inicial:", size=12, weight=ft.FontWeight.W_600, width=65, color=ft.Colors.WHITE),
                        ft.Text(valor_inicial, size=12, color=ft.Colors.WHITE70),
                    ], alignment=ft.MainAxisAlignment.START, spacing=8),
                    ft.Row([
                        ft.Text("Final:", size=12, weight=ft.FontWeight.W_600, width=65, color=ft.Colors.WHITE),
                        ft.Text(valor_final, size=12, color=ft.Colors.WHITE70),
                    ], alignment=ft.MainAxisAlignment.START, spacing=8),
                ], spacing=6, horizontal_alignment=ft.CrossAxisAlignment.START),

                ft.Container(height=10),
                ft.Divider(height=1, color=ft.Colors.WHITE54),
                ft.Container(height=10),

                ft.Column([
                    ft.Text("Variacao:", size=11, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE70),
                    ft.Text(
                        f"{simbolo_variacao}{variacao:.1f} {unidade}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=cor_variacao,
                    ),
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),

            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=18,
            bgcolor=cor,
            border_radius=12,
            width=210,
            height=200,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=6,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
    
    def _exibir_dietas(self):
        self.container_dietas.controls.clear()
        historico = obter_historico_dietas()
        
        if not historico:
            self.container_dietas.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Nenhuma variacao de dieta foi gerada ainda.",
                        size=14,
                        color=ft.Colors.GREY_600,
                        italic=True,
                    ),
                    padding=20,
                )
            )
        else:
            # Identificar dietas de maior e menor calorias
            if len(historico) > 1:
                indice_maior = max(range(len(historico)), key=lambda i: historico[i]['calorias'])
                indice_menor = min(range(len(historico)), key=lambda i: historico[i]['calorias'])
                
                # Criar cards de destaque separados no topo
                cards_destaque = ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.TRENDING_UP, size=24, color=ft.Colors.RED_700),
                                    ft.Text(
                                        "Dieta Mais Calorica",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.RED_900,
                                    ),
                                ], spacing=10),
                                ft.Divider(height=1, color=ft.Colors.RED_300),
                                criar_dieta_card(historico[indice_maior], indice_maior + 1, destaque='maior'),
                            ], spacing=12, tight=True),
                            padding=15,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            border=ft.border.all(2, ft.Colors.RED_200),
                            width=480,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.TRENDING_DOWN, size=24, color=ft.Colors.GREEN_700),
                                    ft.Text(
                                        "Dieta Menos Calorica",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREEN_900,
                                    ),
                                ], spacing=10),
                                ft.Divider(height=1, color=ft.Colors.GREEN_300),
                                criar_dieta_card(historico[indice_menor], indice_menor + 1, destaque='menor'),
                            ], spacing=12, tight=True),
                            padding=15,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            border=ft.border.all(2, ft.Colors.GREEN_200),
                            width=480,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                )
                
                self.container_dietas.controls.append(cards_destaque)
                self.container_dietas.controls.append(ft.Container(height=25))
                
                # Adicionar título para todas as dietas
                self.container_dietas.controls.append(
                    ft.Row([
                        ft.Icon(ft.Icons.LIST, size=22, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Todas as Variacoes de Dietas",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                )
                self.container_dietas.controls.append(ft.Container(height=15))
            

            for idx, dieta in enumerate(historico, 1):

                destaque = None
                if len(historico) > 1:
                    if idx - 1 == indice_maior:
                        destaque = 'maior'
                    elif idx - 1 == indice_menor:
                        destaque = 'menor'
                
                card = criar_dieta_card(dieta, idx, destaque=destaque)
                self.container_dietas.controls.append(card)
        
        self.dietas_wrapper.visible = True
        self.dietas_wrapper.update()

