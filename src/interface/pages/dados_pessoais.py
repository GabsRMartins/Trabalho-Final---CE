"""
Módulo para aba de Dados Pessoais
"""

import flet as ft
from src.entities.individuo import Individuo
from src.interface.util import ValidadorDados, FormularioHelper
from src.interface.components.alert import Alert


class PaginaDadosPessoais:
   
    def __init__(self, callback_validacao, callback_avancar_aba=None):
        self.callback_validacao = callback_validacao
        self.callback_avancar_aba = callback_avancar_aba
        self.individuo = None
        self.dados_validados = None

    def build(self):
        input_width = 340
        
    
        self.txt_peso = ft.TextField(
            label="Peso (kg)",
            hint_text="Ex: 75",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=input_width,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
        )
        self.txt_altura = ft.TextField(
            label="Altura (m)",
            hint_text="Ex: 1.75",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=input_width,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
        )
        self.txt_idade = ft.TextField(
            label="Idade (anos)",
            hint_text="Ex: 30",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=input_width,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
        )
        self.dropdown_sexo = ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("M", "Masculino"),
                ft.dropdown.Option("F", "Feminino"),
            ],
            width=input_width,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
        )
        self.txt_taxa_gordura = ft.TextField(
            label="Taxa de Gordura Corporal (%)",
            hint_text="Ex: 25",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=input_width,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
        )
        self.dropdown_atividade = ft.Dropdown(
            label="Nivel de Atividade",
            options=[
                ft.dropdown.Option("1.2", "Sedentario (pouco exercicio)"),
                ft.dropdown.Option("1.375", "Levemente ativo (1-3 dias/semana)"),
                ft.dropdown.Option("1.55", "Moderadamente ativo (3-5 dias/semana)"),
                ft.dropdown.Option("1.725", "Muito ativo (6-7 dias/semana)"),
                ft.dropdown.Option("1.9", "Extremamente ativo (2x/dia)"),
            ],
            value="1.55",
            width=input_width,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
        )
        self.txt_semanas = ft.TextField(
            label="Numero de Semanas a Simular",
            hint_text="Ex: 36",
            keyboard_type=ft.KeyboardType.NUMBER,
            value="36",
            width=input_width,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
        )

        # Placeholder para alertas
        self.alert_placeholder = ft.Column(controls=[], tight=True)

       
        btn_validar = ft.Container(
            content=ft.ElevatedButton(
                text="Validar e Continuar",
                icon=ft.Icons.CHECK_CIRCLE,
                on_click=self._validar_dados,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            width=input_width,
        )


        form_content = ft.Container(
            content=ft.Column(
                controls=[

                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.PERSON, size=30, color=ft.Colors.BLUE_700),
                                ft.Text(
                                    "Dados Pessoais",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_700,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        margin=ft.margin.only(bottom=20),
                    ),
                    

                    self.alert_placeholder,
                    

                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[

                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.MONITOR_WEIGHT, size=22, color=ft.Colors.BLUE_700),
                                                ft.Text(
                                                    "Informacoes Fisicas",
                                                    size=18,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.BLUE_900,
                                                ),
                                            ],
                                            spacing=8,
                                        ),
                                        ft.Divider(height=1, color=ft.Colors.BLUE_200),
                                        self.txt_peso,
                                        self.txt_altura,
                                        self.txt_idade,
                                        self.dropdown_sexo,
                                        self.txt_taxa_gordura,
                                        
                                        ft.Container(height=15),
                                        

                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.DIRECTIONS_RUN, size=22, color=ft.Colors.ORANGE_700),
                                                ft.Text(
                                                    "Atividade Basal",
                                                    size=18,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.BLUE_900,
                                                ),
                                            ],
                                            spacing=8,
                                        ),
                                        ft.Divider(height=1, color=ft.Colors.ORANGE_200),
                                        self.dropdown_atividade,
                                        
                                        ft.Container(height=15),
                                        

                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.CALENDAR_MONTH, size=22, color=ft.Colors.GREEN_700),
                                                ft.Text(
                                                    "Configuracao da Simulacao",
                                                    size=18,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.BLUE_900,
                                                ),
                                            ],
                                            spacing=8,
                                        ),
                                        ft.Divider(height=1, color=ft.Colors.GREEN_200),
                                        self.txt_semanas,
                                        
                                        ft.Container(height=20),
                                        

                                        btn_validar,
                                    ],
                                    spacing=12,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=30,
                                border_radius=15,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=10,
                                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 2),
                                ),
                                width=450,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=30,
            bgcolor=ft.Colors.GREY_50,
            expand=True,
        )

        return ft.Tab(
            text="Dados Pessoais",
            content=form_content,
        )

    def _validar_dados(self, e):
        """Valida os dados inseridos usando o validador centralizado e exibe alertas"""
        try:
            valido, mensagem_erro, dados_validados = ValidadorDados.validar_todos_dados(
                peso_str=self.txt_peso.value,
                altura_str=self.txt_altura.value,
                idade_str=self.txt_idade.value,
                sexo=self.dropdown_sexo.value or "",
                taxa_gordura_str=self.txt_taxa_gordura.value,
                semanas_str=self.txt_semanas.value,
            )

            if not valido:
                alerta = Alert(f"Erro na validação: {mensagem_erro}", alert_type="error", on_close=self._close_alert)
                self.alert_placeholder.controls = [alerta]
                self.alert_placeholder.update()
                return

           
            self.dados_validados = dados_validados

            
            self.individuo = Individuo(
                peso=dados_validados['peso'],
                altura=dados_validados['altura'],
                idade=dados_validados['idade'],
                sexo=dados_validados['sexo'],
                nivel_atividade=float(self.dropdown_atividade.value or 1.55),
                gasto_treino=0,
                taxa_gordura=dados_validados['taxa_gordura'],
            )

            
            imc = self.individuo.calcular_imc()
            tmb = self.individuo.calcular_tmb()
            tdee = self.individuo.calcular_gasto_calorico_total()

            mensagem = (
                f"Dados Validados com Sucesso!\n\n"
                f"IMC: {imc:.1f} — TMB: {tmb:.0f} kcal/dia — TDEE: {tdee:.0f} kcal/dia\n"
                f"Massa Gorda: {(dados_validados['peso'] * dados_validados['taxa_gordura'] / 100):.1f} kg — "
                f"Massa Magra: {(dados_validados['peso'] * (100 - dados_validados['taxa_gordura']) / 100):.1f} kg"
            )

            alerta = Alert(mensagem, alert_type="success", on_close=self._close_alert, auto_dismiss_seconds=6)
            self.alert_placeholder.controls = [alerta]
            self.alert_placeholder.update()

            
            if self.callback_validacao:
                self.callback_validacao(self.individuo, dados_validados['semanas'])

            
            if self.callback_avancar_aba:
                self.callback_avancar_aba(1) 

        except Exception as ex:
            alerta = Alert(f"Erro inesperado: {str(ex)}", alert_type="error", on_close=self._close_alert)
            self.alert_placeholder.controls = [alerta]
            self.alert_placeholder.update()

    def _close_alert(self, e):
        self.alert_placeholder.controls = []
        try:
            self.alert_placeholder.update()
        except:
            pass

    def get_individuo(self):
        return self.individuo

    def get_semanas(self):
        """Retorna o número de semanas"""
        try:
            return int(self.txt_semanas.value)
        except:
            return 36
