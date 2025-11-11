"""
Módulo para aba de Resultados
"""

import flet as ft
import copy
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg

from src.service.simulation import simular_evolucao
from src.entities.individuo import Individuo

# Usar backend Agg para evitar problemas com display
matplotlib.use('Agg')


class PaginaResultados:
    """Página para execução da simulação e exibição de resultados"""
    
    def __init__(self):
        self.individuo_original = None
        self.alimentos = None
        self.ficha_treino = None
        self.semanas = 36
        
    def build(self):
        """Constrói a aba de Resultados"""
        
        self.txt_status = ft.Text(
            value="Aguardando simulação...",
            size=14,
            color=ft.Colors.ORANGE,
        )
        
        self.progress_bar = ft.ProgressBar(visible=False)
        
        self.container_resultados = ft.Column(spacing=10)
        self.container_graficos = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        btn_executar = ft.ElevatedButton(
            text="🚀 Executar Simulação",
            on_click=self._executar_simulacao,
            bgcolor=ft.Colors.RED_700,
            color="white",
        )
        
        return ft.Tab(
            text="📊 Resultados",
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Simulação de Evolução Corporal", size=18, weight="bold"),
                                self.txt_status,
                                btn_executar,
                                self.progress_bar,
                                ft.Divider(),
                                ft.Text("Resumo Final", size=16, weight="bold"),
                                self.container_resultados,
                                ft.Divider(),
                                ft.Text("Dados de Evolução", size=16, weight="bold"),
                                self.container_graficos,
                            ],
                            spacing=15,
                        ),
                        padding=20,
                    ),
                ],
            ),
        )
    
    def set_parametros_simulacao(self, individuo, alimentos, ficha_treino, semanas):
        """Define os parâmetros para a simulação"""
        self.individuo_original = individuo
        self.alimentos = alimentos
        self.ficha_treino = ficha_treino
        self.semanas = semanas
    
    def _executar_simulacao(self, e):
        """Executa a simulação"""
        if not self.individuo_original or not self.ficha_treino:
            self.txt_status.value = "❌ Complete os dados e escolha uma ficha de treino!"
            self.txt_status.color = ft.Colors.RED
            return
        
        try:
            # Executar simulação
            self.txt_status.value = "⏳ Simulando... Aguarde..."
            self.txt_status.color = ft.Colors.ORANGE
            self.progress_bar.visible = True
            
            # Clonar indivíduo para não modificar original
            individuo_sim = copy.deepcopy(self.individuo_original)
            
            # Simulação
            simular_evolucao(individuo_sim, self.alimentos, self.ficha_treino, self.semanas)
            
            # Exibir resultados
            self._exibir_resultados(individuo_sim)
            
            self.txt_status.value = "✅ Simulação Concluída com Sucesso!"
            self.txt_status.color = ft.Colors.GREEN
            self.progress_bar.visible = False
            
        except Exception as ex:
            self.txt_status.value = f"❌ Erro: {str(ex)}"
            self.txt_status.color = ft.Colors.RED
            self.progress_bar.visible = False
    
    def _exibir_resultados(self, individuo_sim: Individuo):
        """Exibe os resultados da simulação"""
        
        self.container_resultados.controls.clear()
        self.container_graficos.controls.clear()
        
        mudanca_peso = individuo_sim.peso - self.individuo_original.peso
        mudanca_imc = individuo_sim.calcular_imc() - self.individuo_original.calcular_imc()
        mudanca_gordura = individuo_sim.taxa_gordura - self.individuo_original.taxa_gordura
        
        resumo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RESUMO DA EVOLUÇÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏋️ PESO
   Inicial: {self.individuo_original.peso:.1f} kg
   Final: {individuo_sim.peso:.1f} kg
   Variação: {mudanca_peso:+.1f} kg

📐 IMC
   Inicial: {self.individuo_original.calcular_imc():.1f}
   Final: {individuo_sim.calcular_imc():.1f}
   Variação: {mudanca_imc:+.1f}

🔴 TAXA DE GORDURA
   Inicial: {self.individuo_original.taxa_gordura:.1f}%
   Final: {individuo_sim.taxa_gordura:.1f}%
   Variação: {mudanca_gordura:+.1f}%

💪 MASSA MAGRA
   Inicial: {(self.individuo_original.peso * (100 - self.individuo_original.taxa_gordura) / 100):.1f} kg
   Final: {(individuo_sim.peso * (100 - individuo_sim.taxa_gordura) / 100):.1f} kg

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        self.container_resultados.controls.append(
            ft.Text(value=resumo, size=11, font_family="monospace", color=ft.Colors.GREY_800)
        )
        
        try:
            self._criar_graficos_visualizacao(individuo_sim)
        except Exception as ex:
            self.container_graficos.controls.append(
                ft.Text(
                    value=f"⚠️ Erro: {str(ex)}",
                    color=ft.Colors.ORANGE,
                )
            )
    
    def _criar_graficos_visualizacao(self, individuo_sim: Individuo):
        """Cria visualização dos gráficos com matplotlib"""
        
        try:
            # Criar figura com 3 subgráficos
            fig, axes = plt.subplots(3, 1, figsize=(10, 12))
            fig.suptitle("Monitoramento de Evolucao Corporal", fontsize=16, fontweight='bold')
            
            semanas = range(len(individuo_sim.historico_imc))
            
            # ===== Gráfico 1: IMC =====
            ax1 = axes[0]
            ax1.plot(semanas, individuo_sim.historico_imc, color='#1f77b4', linewidth=2.5, marker='o', label='IMC')
            ax1.axhline(y=18.5, color='#2ca02c', linestyle='--', linewidth=1.5, label='IMC Minimo')
            ax1.axhline(y=25, color='#d62728', linestyle='--', linewidth=1.5, label='IMC Maximo')
            ax1.set_ylabel('IMC', fontweight='bold')
            ax1.set_title('Evolucao do IMC', fontsize=12, fontweight='bold')
            ax1.legend(loc='upper right')
            ax1.grid(True, linestyle='--', alpha=0.6)
            ax1.set_facecolor('#fafafa')
            
            # ===== Gráfico 2: Taxa de Gordura =====
            ax2 = axes[1]
            ax2.plot(semanas, individuo_sim.historico_gordura, color='#e377c2', linewidth=2.5, marker='s', label='Taxa de Gordura')
            
            # Linhas de referência por sexo
            if self.individuo_original.sexo.lower() == 'm':
                ax2.axhline(y=6, color='#2ca02c', linestyle='--', linewidth=1.5, label='Minimo (H)')
                ax2.axhline(y=24, color='#d62728', linestyle='--', linewidth=1.5, label='Maximo (H)')
            else:
                ax2.axhline(y=16, color='#2ca02c', linestyle='--', linewidth=1.5, label='Minimo (M)')
                ax2.axhline(y=31, color='#d62728', linestyle='--', linewidth=1.5, label='Maximo (M)')
            
            ax2.set_ylabel('Taxa de Gordura (%)', fontweight='bold')
            ax2.set_title('Evolucao da Taxa de Gordura Corporal', fontsize=12, fontweight='bold')
            ax2.legend(loc='upper right')
            ax2.grid(True, linestyle='--', alpha=0.6)
            ax2.set_facecolor('#fafafa')
            
            # ===== Gráfico 3: Calorias =====
            ax3 = axes[2]
            ax3.plot(semanas, individuo_sim.historico_calorias, color='#2ca02c', linewidth=2.5, marker='^', label='Calorias Diarias')
            ax3.set_xlabel('Semanas', fontweight='bold')
            ax3.set_ylabel('Calorias (kcal)', fontweight='bold')
            ax3.set_title('Evolucao da Ingestao Calorica Diaria', fontsize=12, fontweight='bold')
            ax3.legend(loc='upper right')
            ax3.grid(True, linestyle='--', alpha=0.6)
            ax3.set_facecolor('#fafafa')
            
            # Ajustes finais
            for ax in axes:
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            
            # Converter figura para imagem base64
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            plt.close(fig)
            
            # Adicionar imagem ao container
            image_widget = ft.Image(
                src_base64=image_base64,
                width=800,
                height=900,
                fit=ft.ImageFit.CONTAIN,
            )
            
            self.container_graficos.controls.append(
                ft.Container(
                    content=image_widget,
                    padding=10,
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=10,
                )
            )
            
        except Exception as ex:
            self.container_graficos.controls.append(
                ft.Text(
                    value=f"Aviso ao gerar graficos: {str(ex)}",
                    color=ft.Colors.ORANGE,
                )
            )
