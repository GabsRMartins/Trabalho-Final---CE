"""
Módulo para aba de Informações
"""

import flet as ft


class PaginaInformacoes:
    """Página com informações sobre a aplicação"""
    
    def build(self):
        """Constrói a aba de Informações"""
        
        texto_info = """
🔬 SOBRE A SIMULAÇÃO

Esta aplicação simula a evolução corporal de um indivíduo ao longo de semanas, considerando:

✅ Cálculo do Gasto Calórico (Harris-Benedict)
✅ Otimização Genética de Seleção de Alimentos
✅ Diferentes Fichas de Treino (ABC, ABCD, PPL)
✅ Mudanças de Composição Corporal
✅ Ajustes Metabólicos Dinâmicos

📚 FONTES CIENTÍFICAS

• Harris-Benedict (1919) - Taxa Metabólica Basal
• Compendium of Physical Activities (2024) - METs
• Jackson & Pollock (1978) - Composição Corporal
• WHO (1995) - Índice de Massa Corporal

🔧 TECNOLOGIA

• Flet - Interface Gráfica
• Algoritmo Genético - Otimização de Dieta
• Matplotlib - Visualização de Gráficos
• Python 3.10+

⚠️ AVISO IMPORTANTE

Esta é uma simulação educacional para fins acadêmicos. 
Não deve ser usada para prescrição nutricional ou médica.

📧 Documentação: FONTES_CIENTIFICAS.md, VALIDACAO_FONTES.md
        """
        
        return ft.Tab(
            text="ℹ️ Informações",
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        content=ft.Text(
                            value=texto_info,
                            size=12,
                            color=ft.Colors.GREY_800,
                        ),
                        padding=20,
                    ),
                ],
            ),
        )
