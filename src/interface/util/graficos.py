
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
from src.entities.individuo import Individuo

matplotlib.use('Agg')


def criar_graficos_evolucao(individuo_original: Individuo, individuo_sim: Individuo):

    
    try:
        # Criar figura com 3 subgráficos
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        fig.suptitle("Monitoramento de Evolução Corporal", fontsize=16, fontweight='bold', y=0.995)
        
        semanas = range(len(individuo_sim.historico_imc))
        
        # ===== Gráfico 1: IMC =====
        ax1 = axes[0]
        ax1.plot(semanas, individuo_sim.historico_imc, color='#1f77b4', linewidth=2.5, marker='o', markersize=6, label='IMC')
        ax1.axhline(y=18.5, color='#2ca02c', linestyle='--', linewidth=1.5, label='IMC Mínimo (18.5)')
        ax1.axhline(y=25, color='#d62728', linestyle='--', linewidth=1.5, label='IMC Máximo (25)')
        ax1.fill_between(semanas, 18.5, 25, alpha=0.1, color='#2ca02c')
        ax1.set_ylabel('IMC', fontweight='bold', fontsize=11)
        ax1.set_title('Evolução do IMC', fontsize=12, fontweight='bold', pad=10)
        ax1.legend(loc='best', fontsize=9)
        ax1.grid(True, linestyle='--', alpha=0.4)
        ax1.set_facecolor('#fafafa')
        
        # ===== Gráfico 2: Taxa de Gordura =====
        ax2 = axes[1]
        ax2.plot(semanas, individuo_sim.historico_gordura, color='#e377c2', linewidth=2.5, marker='s', markersize=6, label='Taxa de Gordura')
        
        # Linhas de referência por sexo
        if individuo_original.sexo.lower() == 'm':
            ax2.axhline(y=6, color='#2ca02c', linestyle='--', linewidth=1.5, label='Mínimo (H): 6%')
            ax2.axhline(y=24, color='#d62728', linestyle='--', linewidth=1.5, label='Máximo (H): 24%')
            ax2.fill_between(semanas, 6, 24, alpha=0.1, color='#e377c2')
        else:
            ax2.axhline(y=16, color='#2ca02c', linestyle='--', linewidth=1.5, label='Mínimo (M): 16%')
            ax2.axhline(y=31, color='#d62728', linestyle='--', linewidth=1.5, label='Máximo (M): 31%')
            ax2.fill_between(semanas, 16, 31, alpha=0.1, color='#e377c2')
        
        ax2.set_ylabel('Taxa de Gordura (%)', fontweight='bold', fontsize=11)
        ax2.set_title('Evolução da Taxa de Gordura Corporal', fontsize=12, fontweight='bold', pad=10)
        ax2.legend(loc='best', fontsize=9)
        ax2.grid(True, linestyle='--', alpha=0.4)
        ax2.set_facecolor('#fafafa')
        
        # ===== Gráfico 3: Calorias =====
        ax3 = axes[2]
        ax3.plot(semanas, individuo_sim.historico_calorias, color='#ff7f0e', linewidth=2.5, marker='^', markersize=6, label='Calorias Diárias')
        ax3.fill_between(semanas, 0, individuo_sim.historico_calorias, alpha=0.2, color='#ff7f0e')
        ax3.set_xlabel('Semanas', fontweight='bold', fontsize=11)
        ax3.set_ylabel('Calorias (kcal)', fontweight='bold', fontsize=11)
        ax3.set_title('Evolução da Ingestão Calórica Diária', fontsize=12, fontweight='bold', pad=10)
        ax3.legend(loc='best', fontsize=9)
        ax3.grid(True, linestyle='--', alpha=0.4)
        ax3.set_facecolor('#fafafa')
        
        # Ajustes finais
        for ax in axes:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        
        # Converter para base64
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)
        
        return image_base64
        
    except Exception as ex:
        raise Exception(f"Erro ao gerar gráficos: {str(ex)}")
