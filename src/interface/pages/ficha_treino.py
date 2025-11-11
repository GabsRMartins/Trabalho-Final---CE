"""
Módulo para aba de Ficha de Treino
"""

import flet as ft
from src.entities.treino import FichaTreino


class PaginaFichaTreino:
    """Página para seleção de ficha de treino"""
    
    def __init__(self, callback_confirmacao):
        self.callback_confirmacao = callback_confirmacao
        self.ficha_treino = None
        self.peso_individuo = 70  # Peso padrão para referência
        
    def build(self):
        """Constrói a aba de Ficha de Treino"""
        
        self.radio_treino = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value="ABC", label="📅 Divisão ABC (3 dias)"),
                    ft.Radio(value="ABCD", label="📅 Divisão ABCD (4 dias)"),
                    ft.Radio(value="PPL", label="📅 Push/Pull/Legs (PPL)"),
                ],
                spacing=10,
            ),
            value="ABC",
            on_change=self._on_treino_change,
        )
        
        self.txt_descricao = ft.Text(
            value=self._get_descricao("ABC"),
            size=12,
            color=ft.Colors.GREY_700,
        )
        
        self.txt_status = ft.Text(
            value="",
            size=14,
            color=ft.Colors.ORANGE,
        )
        
        btn_confirmar = ft.ElevatedButton(
            text="✅ Confirmar Ficha de Treino",
            on_click=self._confirmar_treino,
            bgcolor=ft.Colors.BLUE,
            color="white",
        )
        
        return ft.Tab(
            text="💪 Ficha de Treino",
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Escolha uma Ficha de Treino", size=18, weight="bold"),
                                self.radio_treino,
                                ft.Container(
                                    content=self.txt_descricao,
                                    padding=15,
                                    bgcolor=ft.Colors.GREY_100,
                                    border_radius=10,
                                ),
                                btn_confirmar,
                                self.txt_status,
                            ],
                            spacing=15,
                        ),
                        padding=20,
                    ),
                ],
            ),
        )
    
    def _on_treino_change(self, e):
        """Atualiza descrição ao mudar seleção"""
        tipo = self.radio_treino.value
        self.txt_descricao.value = self._get_descricao(tipo)
    
    def _confirmar_treino(self, e):
        """Confirma a ficha de treino"""
        tipo_divisao = self.radio_treino.value
        self.ficha_treino = FichaTreino(tipo_divisao=tipo_divisao)
        
        gasto_semanal = self.ficha_treino.calcular_gasto_semanal(self.peso_individuo)
        gasto_diario = self.ficha_treino.calcular_gasto_diario_medio(self.peso_individuo)
        
        self.txt_status.value = f"""✅ Ficha de Treino Confirmada!

💪 Tipo: {tipo_divisao}
📈 Gasto Semanal: {gasto_semanal:.0f} kcal
📊 Gasto Diário (Média): {gasto_diario:.0f} kcal

👉 Próximo: Execute a Simulação"""
        self.txt_status.color = ft.Colors.GREEN
        
        if self.callback_confirmacao:
            self.callback_confirmacao(self.ficha_treino)
    
    def _get_descricao(self, tipo: str) -> str:
        """Retorna descrição da ficha"""
        descricoes = {
            "ABC": "📅 DIVISÃO ABC (3 DIAS)\n\n• SEGUNDA (A): Musculação Superior\n• TERÇA (B): Musculação Inferior\n• QUINTA (C): Treino Funcional/HIIT\n\n💡 Ideal para iniciantes",
            "ABCD": "📅 DIVISÃO ABCD (4 DIAS)\n\n• SEGUNDA (A): Musculação Superior\n• TERÇA (B): Musculação Inferior\n• QUINTA (C): Treino Funcional\n• SEXTA (D): Cardio Moderado\n\n💡 Intermediária",
            "PPL": "📅 PPL - PUSH/PULL/LEGS\n\n• SEGUNDA (PUSH): Peito, Ombros, Tríceps\n• TERÇA (PULL): Costas, Bíceps\n• QUINTA (LEGS): Quadríceps, Glúteos\n\n💡 Avançada",
        }
        return descricoes.get(tipo, "")
    
    def get_ficha_treino(self):
        """Retorna a ficha de treino confirmada"""
        return self.ficha_treino
    
    def set_peso_individuo(self, peso):
        """Define o peso do indivíduo para cálculos"""
        self.peso_individuo = peso
