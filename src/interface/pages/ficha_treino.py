"""
Módulo para aba de Ficha de Treino
"""

import flet as ft
from src.entities.treino import FichaTreino, TipoTreino
from src.interface.components.alert import Alert
from src.interface.util import ValidadorTreino


class PaginaFichaTreino:
   
    
    def __init__(self, callback_confirmacao, callback_avancar_aba=None):
        self.callback_confirmacao = callback_confirmacao
        self.callback_avancar_aba = callback_avancar_aba
        self.ficha_treino = None
        self.treino_personalizado = {}  
        
    def build(self):
        
        self.radio_treino = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Radio(value="ABC", label="Divisao ABC (3 dias)"),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.BLUE_200),
                    ),
                    ft.Container(
                        content=ft.Radio(value="ABCD", label="Divisao ABCD (4 dias)"),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.BLUE_200),
                    ),
                    ft.Container(
                        content=ft.Radio(value="PPL", label="Push/Pull/Legs (PPL)"),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.BLUE_200),
                    ),
                    ft.Container(
                        content=ft.Radio(value="PERSONALIZADO", label="Treino Personalizado"),
                        bgcolor=ft.Colors.GREEN_50,
                        padding=10,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.GREEN_200),
                    ),
                ],
                spacing=8,
            ),
            value="ABC",
            on_change=self._on_treino_change,
        )
        
        self.container_personalizado = ft.Column(
            controls=[],
            visible=False,
            spacing=10,
        )
        

        self.txt_descricao = ft.Text(
            value=self._get_descricao("ABC"),
            size=14,
            color=ft.Colors.GREY_800,
            weight=ft.FontWeight.W_500,
        )
        

        self.alert_placeholder = ft.Column(controls=[], tight=True)
        

        btn_confirmar = ft.Container(
            content=ft.ElevatedButton(
                text="Confirmar Ficha de Treino",
                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                on_click=self._confirmar_treino,
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            width=350,
        )
        
 
        form_content = ft.Container(
            content=ft.Column(
                controls=[

                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.FITNESS_CENTER, size=30, color=ft.Colors.BLUE_700),
                                ft.Text(
                                    "Escolha sua Ficha de Treino",
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
                                        ft.Text(
                                            "Tipo de Treino",
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_900,
                                        ),
                                        ft.Divider(height=1, color=ft.Colors.BLUE_200),
                                        self.radio_treino,
                                        ft.Container(height=10),
                                        self.container_personalizado,
                                        ft.Container(height=15),
                                        btn_confirmar,
                                    ],
                                    spacing=12,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=25,
                                border_radius=15,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=8,
                                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 2),
                                ),
                                width=420,
                            ),
                            
                            # Coluna direita - Descrição
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.INFO_OUTLINE, size=22, color=ft.Colors.BLUE_700),
                                                ft.Text(
                                                    "Detalhes do Treino",
                                                    size=17,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.BLUE_900,
                                                ),
                                            ],
                                            spacing=8,
                                        ),
                                        ft.Divider(height=1, color=ft.Colors.BLUE_200),
                                        ft.Container(
                                            content=self.txt_descricao,
                                            padding=18,
                                            bgcolor=ft.Colors.BLUE_50,
                                            border_radius=12,
                                            border=ft.border.all(1, ft.Colors.BLUE_100),
                                        ),
                                    ],
                                    spacing=12,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=20,
                                border_radius=15,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=8,
                                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 2),
                                ),
                                width=450,
                            ),
                        ],
                        spacing=20,
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
            text="Ficha de Treino",
            content=form_content,
        )
    
    def _on_treino_change(self, e):
        tipo = self.radio_treino.value
        self.txt_descricao.value = self._get_descricao(tipo)
        
        
        if tipo == "PERSONALIZADO":
            self.container_personalizado.visible = True
            self._criar_formulario_personalizado()
        else:
            self.container_personalizado.visible = False
            
        self.txt_descricao.update()
        self.container_personalizado.update()
    
    def _confirmar_treino(self, e):
        try:
            tipo_divisao = self.radio_treino.value
            
            if tipo_divisao == "PERSONALIZADO":
            
                valido, mensagem_erro = ValidadorTreino.validar_treino_personalizado(self.treino_personalizado)
                if not valido:
                    alerta = Alert(mensagem_erro, alert_type="error", on_close=self._close_alert)
                    self.alert_placeholder.controls = [alerta]
                    self.alert_placeholder.update()
                    return
                
                # Criar ficha com tipo base e depois substituir treinos
                self.ficha_treino = FichaTreino(tipo_divisao="ABC")
                self.ficha_treino.treinos = self.treino_personalizado.copy()
                tipo_nome = "Personalizado"
            else:
                self.ficha_treino = FichaTreino(tipo_divisao=tipo_divisao)
                tipo_nome = tipo_divisao
            
            gasto_semanal = self.ficha_treino.calcular_gasto_semanal(self.peso_individuo)
            gasto_diario = self.ficha_treino.calcular_gasto_diario_medio(self.peso_individuo)
            
            mensagem = (
                f"Ficha de Treino Confirmada!\n\n"
                f"Tipo: {tipo_nome}\n"
                f"Gasto Semanal: {gasto_semanal:.0f} kcal\n"
                f"Gasto Diario (Media): {gasto_diario:.0f} kcal"
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
            "ABC": "DIVISAO ABC (3 DIAS)\n\n• SEGUNDA (A): Musculacao Superior\n• TERCA (B): Musculacao Inferior\n• QUINTA (C): Treino Funcional/HIIT\n• DEMAIS DIAS: Repouso\n\nIdeal para iniciantes que estao comecando no treino.",
            "ABCD": "DIVISAO ABCD (4 DIAS)\n\n• SEGUNDA (A): Musculacao Superior\n• TERCA (B): Musculacao Inferior\n• QUINTA (C): Treino Funcional\n• SEXTA (D): Cardio Moderado\n• DEMAIS DIAS: Repouso\n\nNivel intermediario, bom equilibrio treino/descanso.",
            "PPL": "PPL - PUSH/PULL/LEGS\n\n• SEGUNDA (PUSH): Peito, Ombros, Triceps\n• TERCA (PULL): Costas, Biceps\n• QUINTA (LEGS): Quadriceps, Gluteos\n• SABADO: Cardio Leve\n• DEMAIS DIAS: Repouso\n\nNivel avancado, alto volume de treino.",
            "PERSONALIZADO": "TREINO PERSONALIZADO\n\nConfigure cada dia da semana com o tipo de treino desejado.\n\nOpcoes disponiveis:\n• Superior - Musculacao peito/costas/ombros (3.0 MET)\n• Inferior - Musculacao pernas (4.0 MET)\n• Perna Intensa - Agachamentos pesados (4.5 MET)\n• Cardio Leve/Moderado/Intenso (2.5-5.0 MET)\n• Funcional/HIIT (4.25 MET)\n• Yoga (1.5 MET)\n• Repouso (1.0 MET)\n\nLembre-se: Inclua pelo menos 1 dia de repouso!",
        }
        return descricoes.get(tipo, "")
    
    def get_ficha_treino(self):
        return self.ficha_treino
    
    def set_peso_individuo(self, peso):

        self.peso_individuo = peso
    
    def _criar_formulario_personalizado(self):
        """Cria formulário para configurar treino personalizado"""
        
        dias_semana = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
        

        opcoes_treino = [
            ("SUPERIOR", "Superior (3.0 MET)"),
            ("INFERIOR", "Inferior (4.0 MET)"),
            ("PERNA_INTENSA", "Perna Intensa (4.5 MET)"),
            ("CARDIO_LEVE", "Cardio Leve (2.5 MET)"),
            ("CARDIO_MODERADO", "Cardio Moderado (3.75 MET)"),
            ("CARDIO_INTENSO", "Cardio Intenso (5.0 MET)"),
            ("FUNCIONAL", "Funcional/HIIT (4.25 MET)"),
            ("YOGA", "Yoga (1.5 MET)"),
            ("REPOUSO", "Repouso (1.0 MET)"),
        ]
        

        self.container_personalizado.controls.clear()
        

        self.container_personalizado.controls.append(
            ft.Text("Configure cada dia:", size=14, weight="bold", color=ft.Colors.BLUE_700)
        )
        

        self.dropdowns_dias = {}
        for i, dia in enumerate(dias_semana):
            dropdown = ft.Dropdown(
                label=dia,
                options=[ft.dropdown.Option(key=op[0], text=op[1]) for op in opcoes_treino],
                value="REPOUSO",
                width=300,
                dense=True,
                on_change=lambda e, d=dia: self._atualizar_treino_dia(d, e.control.value),
            )
            self.dropdowns_dias[dia] = dropdown
            self.container_personalizado.controls.append(dropdown)
        

        self.treino_personalizado = {dia: TipoTreino.REPOUSO for dia in dias_semana}
    
    def _atualizar_treino_dia(self, dia: str, tipo_treino_nome: str):

        
        try:

            tipo_treino = TipoTreino[tipo_treino_nome]
            self.treino_personalizado[dia] = tipo_treino
        except KeyError:
            pass 

