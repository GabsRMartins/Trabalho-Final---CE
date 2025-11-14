"""
Módulo para aba de Ficha de Treino
"""

import flet as ft
from src.entities.treino import FichaTreino
from src.interface.components.alert import Alert


class PaginaFichaTreino:
   
    
    def __init__(self, callback_confirmacao, callback_avancar_aba=None):
        self.callback_confirmacao = callback_confirmacao
        self.callback_avancar_aba = callback_avancar_aba
        self.ficha_treino = None
        self.peso_individuo = 70 
        
    def build(self):

        
        self.radio_treino = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value="ABC", label="Divisão ABC (3 dias)"),
                    ft.Radio(value="ABCD", label="Divisão ABCD (4 dias)"),
                    ft.Radio(value="PPL", label="Push/Pull/Legs (PPL)"),
                ],
                spacing=12,
            ),
            value="ABC",
            on_change=self._on_treino_change,
        )
        
        self.txt_descricao = ft.Text(
            value=self._get_descricao("ABC"),
            size=12,
            color=ft.Colors.GREY_700,
        )
        

        self.alert_placeholder = ft.Column(controls=[], tight=True)
        
        btn_confirmar = ft.ElevatedButton(
            text="Confirmar Ficha de Treino",
            on_click=self._confirmar_treino,
            bgcolor=ft.Colors.BLUE,
            color="white",
            width=320,
        )
        
     
        form_content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=20),  
                ft.Text("Escolha uma Ficha de Treino", size=22, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                self.alert_placeholder,
                ft.Container(
                    content=ft.Row([
             
                        ft.Column([
                            self.radio_treino,
                            ft.Container(height=15),
                            btn_confirmar,
                        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=350),
                        
                        ft.VerticalDivider(),
                        
                
                        ft.Column([
                            ft.Container(
                                content=self.txt_descricao,
                                padding=15,
                                bgcolor=ft.Colors.GREY_100,
                                border_radius=10,
                                expand=True,
                            ),
                        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True, width=350),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                    padding=ft.padding.symmetric(horizontal=20, vertical=20),
                ),
                ft.Container(height=20), 
            ],
        )
        
        return ft.Tab(
            text="Ficha de Treino",
            content=form_content,
        )
    
    def _on_treino_change(self, e):
        tipo = self.radio_treino.value
        self.txt_descricao.value = self._get_descricao(tipo)
        self.txt_descricao.update()
    
    def _confirmar_treino(self, e):
        try:
            tipo_divisao = self.radio_treino.value
            self.ficha_treino = FichaTreino(tipo_divisao=tipo_divisao)
            
            gasto_semanal = self.ficha_treino.calcular_gasto_semanal(self.peso_individuo)
            gasto_diario = self.ficha_treino.calcular_gasto_diario_medio(self.peso_individuo)
            
            mensagem = (
                f"Ficha de Treino Confirmada!\n\n"
                f"Tipo: {tipo_divisao}\n"
                f"Gasto Semanal: {gasto_semanal:.0f} kcal\n"
                f"Gasto Diário (Média): {gasto_diario:.0f} kcal"
            )
            
            alerta = Alert(mensagem, alert_type="success", on_close=self._close_alert, auto_dismiss_seconds=6)
            self.alert_placeholder.controls = [alerta]
            self.alert_placeholder.update()
            
            if self.callback_confirmacao:
                self.callback_confirmacao(self.ficha_treino)

            if self.callback_avancar_aba:
                self.callback_avancar_aba(2)  
        except Exception as ex:
            alerta = Alert(f"Erro ao confirmar ficha: {str(ex)}", alert_type="error", on_close=self._close_alert)
            self.alert_placeholder.controls = [alerta]
            self.alert_placeholder.update()
    
    def _close_alert(self, e):

        self.alert_placeholder.controls = []
        try:
            self.alert_placeholder.update()
        except:
            pass
    
    def _get_descricao(self, tipo: str) -> str:
        descricoes = {
            "ABC": "DIVISÃO ABC (3 DIAS)\n\n• SEGUNDA (A): Musculação Superior\n• TERÇA (B): Musculação Inferior\n• QUINTA (C): Treino Funcional/HIIT\n\nIdeal para iniciantes",
            "ABCD": "DIVISÃO ABCD (4 DIAS)\n\n• SEGUNDA (A): Musculação Superior\n• TERÇA (B): Musculação Inferior\n• QUINTA (C): Treino Funcional\n• SEXTA (D): Cardio Moderado\n\nIntermediária",
            "PPL": "PPL - PUSH/PULL/LEGS\n\n• SEGUNDA (PUSH): Peito, Ombros, Tríceps\n• TERÇA (PULL): Costas, Bíceps\n• QUINTA (LEGS): Quadríceps, Glúteos\n\nAvançada",
        }
        return descricoes.get(tipo, "")
    
    def get_ficha_treino(self):
        return self.ficha_treino
    
    def set_peso_individuo(self, peso):

        self.peso_individuo = peso

