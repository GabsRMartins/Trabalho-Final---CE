"""
Módulo para aba de Resultados
"""

import flet as ft
import copy

from src.service.simulation import simular_evolucao
from src.entities.individuo import Individuo
from src.interface.util.graficos import criar_graficos_evolucao


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
            value="Aguardando simulação...",
            size=13,
            color=ft.Colors.ORANGE,
        )
        
        self.progress_bar = ft.ProgressBar(visible=False)
        
        self.container_resumo = ft.Row(spacing=15, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        self.container_graficos = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Container wrapper para o resumo
        self.resumo_wrapper = ft.Container(
            content=ft.Column([
                ft.Text("Resumo da Evolução", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                self.container_resumo,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            visible=False,
        )
        
        # Container wrapper para os gráficos
        self.graficos_wrapper = ft.Container(
            content=ft.Column([
                ft.Text("Dados de Evolução", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                self.container_graficos,
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            visible=False,
        )
        
        self.btn_executar = ft.ElevatedButton(
            text="Executar Simulação",
            on_click=self._executar_simulacao,
            bgcolor=ft.Colors.RED_700,
            color="white",
            width=320,
        )
        
        # Layout centralizado com scroll
        self.content_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=20),
                ft.Text("Simulação de Evolução Corporal", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                self.alert_placeholder,
                self.txt_status,
                ft.Container(height=10),
                self.btn_executar,
                self.progress_bar,
                ft.Container(height=20),
                self.resumo_wrapper,
                self.graficos_wrapper,
                ft.Container(height=20),
            ],
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
            
            self.txt_status.value = "Simulando... Aguarde..."
            self.txt_status.color = ft.Colors.ORANGE
            self.progress_bar.visible = True
            self.txt_status.update()
            self.progress_bar.update()
            
            individuo_sim = copy.deepcopy(self.individuo_original)
            simular_evolucao(individuo_sim, self.alimentos, self.ficha_treino, self.semanas)
            
            self._exibir_resultados(individuo_sim)
            
            self.txt_status.value = "Simulação Concluída com Sucesso!"
            self.txt_status.color = ft.Colors.GREEN
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
        """Callback para fechar o alerta"""
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
    
    def _criar_card_resumo(self, titulo: str, valor_inicial: str, valor_final: str, variacao: float, unidade: str, cor: str) -> ft.Container:
   
        cor_variacao = ft.Colors.GREEN if variacao >= 0 else ft.Colors.RED
        simbolo_variacao = "+" if variacao >= 0 else ""
        
        if titulo == "Taxa de Gordura" and variacao < 0:
            cor_variacao = ft.Colors.GREEN
            simbolo_variacao = ""
        
        return ft.Container(
            content=ft.Column([
        ft.Text(titulo, size=14, weight="bold", text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE),
        ft.Container(height=5),

        ft.Column([
            ft.Row([
                ft.Text("Inicial:", size=11, weight="bold", width=80, color=ft.Colors.WHITE),
                ft.Text(valor_inicial, size=11, color=ft.Colors.WHITE),
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            ft.Row([
                ft.Text("Final:", size=11, weight="bold", width=80, color=ft.Colors.WHITE),
                ft.Text(valor_final, size=11, color=ft.Colors.WHITE),
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
        ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.START),

        ft.Container(height=8),
        ft.Divider(height=1, color=ft.Colors.WHITE70),
        ft.Container(height=8),

        ft.Row([
            ft.Text("Variação:", size=11, weight="bold", color=ft.Colors.WHITE),
            ft.Text(
                f"{simbolo_variacao}{variacao:.1f} {unidade}",
                size=13, weight="bold", color=cor_variacao
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),

    ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    padding=15,
    bgcolor=cor,
    border_radius=10,
    opacity=0.9,
    width=200,
    height=180,
        )

