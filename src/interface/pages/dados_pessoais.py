"""
Módulo para aba de Dados Pessoais
"""

import flet as ft
from src.entities.individuo import Individuo
from src.interface.util import ValidadorDados, FormularioHelper


class PaginaDadosPessoais:
    """Página para entrada de dados pessoais do usuário"""
    
    def __init__(self, callback_validacao, callback_avancar_aba=None):
        self.callback_validacao = callback_validacao
        self.callback_avancar_aba = callback_avancar_aba
        self.individuo = None
        self.dados_validados = None
        
    def build(self):
        """Constrói a aba de Dados Pessoais"""
        
        # Campos de entrada
        self.txt_peso = ft.TextField(
            label="Peso (kg)",
            hint_text="Ex: 75",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        self.txt_altura = ft.TextField(
            label="Altura (m)",
            hint_text="Ex: 1.75",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        self.txt_idade = ft.TextField(
            label="Idade (anos)",
            hint_text="Ex: 30",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        self.dropdown_sexo = ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("M", "Masculino"),
                ft.dropdown.Option("F", "Feminino"),
            ],
        )
        
        self.txt_taxa_gordura = ft.TextField(
            label="Taxa de Gordura Corporal (%)",
            hint_text="Ex: 25",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        self.dropdown_atividade = ft.Dropdown(
            label="Nível de Atividade",
            options=[
                ft.dropdown.Option("1.2", "Sedentário (pouco exercício)"),
                ft.dropdown.Option("1.375", "Levemente ativo (1-3 dias/semana)"),
                ft.dropdown.Option("1.55", "Moderadamente ativo (3-5 dias/semana)"),
                ft.dropdown.Option("1.725", "Muito ativo (6-7 dias/semana)"),
                ft.dropdown.Option("1.9", "Extremamente ativo (2x/dia)"),
            ],
            value="1.55",
        )
        
        self.txt_semanas = ft.TextField(
            label="Número de Semanas a Simular",
            hint_text="Ex: 36",
            keyboard_type=ft.KeyboardType.NUMBER,
            value="36",
        )
        
        self.txt_status = ft.Text(
            value="",
            size=14,
            color=ft.Colors.ORANGE,
        )
        
        btn_validar = ft.ElevatedButton(
            text="Validar Dados",
            on_click=self._validar_dados,
            bgcolor=ft.Colors.GREEN,
            color="white",
        )
        
        return ft.Tab(
            text="Dados Pessoais",
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Insira Seus Dados Pessoais", size=18, weight="bold"),
                                self.txt_peso,
                                self.txt_altura,
                                self.txt_idade,
                                self.dropdown_sexo,
                                self.txt_taxa_gordura,
                                ft.Divider(),
                                ft.Text("Atividade Basal", size=14, weight="bold"),
                                self.dropdown_atividade,
                                ft.Divider(),
                                ft.Text("Configuracao da Simulacao", size=14, weight="bold"),
                                self.txt_semanas,
                                btn_validar,
                                self.txt_status,
                            ],
                            spacing=15,
                        ),
                        padding=20,
                    ),
                ],
            ),
        )
    
    def _validar_dados(self, e):
        """Valida os dados inseridos usando o validador centralizado"""
        try:
            # Usar validador centralizado para validar todos os dados
            valido, mensagem_erro, dados_validados = ValidadorDados.validar_todos_dados(
                peso_str=self.txt_peso.value,
                altura_str=self.txt_altura.value,
                idade_str=self.txt_idade.value,
                sexo=self.dropdown_sexo.value or "",
                taxa_gordura_str=self.txt_taxa_gordura.value,
                semanas_str=self.txt_semanas.value,
            )
            
            if not valido:
                self.txt_status.value = f"Erro na validacao:\n{mensagem_erro}"
                self.txt_status.color = ft.Colors.RED
                return
            
            # Armazenar dados validados
            self.dados_validados = dados_validados
            
            # Criar indivíduo com dados validados
            self.individuo = Individuo(
                peso=dados_validados['peso'],
                altura=dados_validados['altura'],
                idade=dados_validados['idade'],
                sexo=dados_validados['sexo'],
                nivel_atividade=float(self.dropdown_atividade.value or 1.55),
                gasto_treino=0,
                taxa_gordura=dados_validados['taxa_gordura'],
            )
            
            # Calcular informações
            imc = self.individuo.calcular_imc()
            tmb = self.individuo.calcular_tmb()
            tdee = self.individuo.calcular_gasto_calorico_total()
            
            self.txt_status.value = f"""Dados Validados com Sucesso!

Calculos:
• IMC: {imc:.1f}
• TMB: {tmb:.0f} kcal/dia
• TDEE: {tdee:.0f} kcal/dia
• Massa Gorda: {(dados_validados['peso'] * dados_validados['taxa_gordura'] / 100):.1f} kg
• Massa Magra: {(dados_validados['peso'] * (100 - dados_validados['taxa_gordura']) / 100):.1f} kg

Proximo: Selecione uma Ficha de Treino"""
            self.txt_status.color = ft.Colors.GREEN
            
            # Chamar callback com dados validados
            if self.callback_validacao:
                self.callback_validacao(self.individuo, dados_validados['semanas'])
            
            # Avançar automaticamente para próxima aba (Ficha de Treino)
            if self.callback_avancar_aba:
                self.callback_avancar_aba(1)  # Índice 1 = Ficha de Treino
            
        except Exception as ex:
            self.txt_status.value = f"Erro inesperado: {str(ex)}"
            self.txt_status.color = ft.Colors.RED
    
    def get_individuo(self):
        """Retorna o indivíduo validado"""
        return self.individuo
    
    def get_semanas(self):
        """Retorna o número de semanas"""
        try:
            return int(self.txt_semanas.value)
        except:
            return 36
