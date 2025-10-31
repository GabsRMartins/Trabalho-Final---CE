import matplotlib.pyplot as plt
import seaborn as sns

def plotar_evolucao(individuo):
    semanas = range(len(individuo.historico_imc))

    # Estilo moderno
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans'],
        'axes.titlesize': 16,
        'axes.labelsize': 13,
        'legend.fontsize': 11,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'axes.linewidth': 1.2
    })

    # Criar figura
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    fig.suptitle("Monitoramento de Saúde ao Longo das Semanas", fontsize=18, fontweight='bold', color='#333333')

    # ---------- IMC ----------
    ax1 = axes[0]
    ax1.plot(semanas, individuo.historico_imc, color='#1f77b4', linewidth=2.5, marker='o', label='IMC')
    ax1.axhline(y=18.5, color='#2ca02c', linestyle='--', linewidth=1.5, label='IMC Mínimo Saudável')
    ax1.axhline(y=25, color='#d62728', linestyle='--', linewidth=1.5, label='IMC Máximo Saudável')
    ax1.set_ylabel('IMC')
    ax1.set_title('Evolução do IMC', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', frameon=True, shadow=True)
    
    # ---------- Taxa de Gordura ----------
    ax2 = axes[1]
    ax2.plot(semanas, individuo.historico_gordura, color='#e377c2', linewidth=2.5, marker='s', label='Taxa de Gordura')
    if individuo.sexo.lower() == 'm':
        ax2.axhline(y=6, color='#2ca02c', linestyle='--', linewidth=1.5, label='Mínimo Saudável (H)')
        ax2.axhline(y=24, color='#d62728', linestyle='--', linewidth=1.5, label='Máximo Saudável (H)')
    else:
        ax2.axhline(y=16, color='#2ca02c', linestyle='--', linewidth=1.5, label='Mínimo Saudável (M)')
        ax2.axhline(y=31, color='#d62728', linestyle='--', linewidth=1.5, label='Máximo Saudável (M)')
    ax2.set_ylabel('Taxa de Gordura (%)')
    ax2.set_title('Evolução da Taxa de Gordura Corporal', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right', frameon=True, shadow=True)

    # ---------- Calorias ----------
    ax3 = axes[2]
    ax3.plot(semanas, individuo.historico_calorias, color='#2ca02c', linewidth=2.5, marker='^', label='Calorias Diárias')
    ax3.set_xlabel('Semanas')
    ax3.set_ylabel('Calorias')
    ax3.set_title('Evolução da Ingestão Calórica Diária', fontsize=14, fontweight='bold')
    ax3.legend(loc='upper right', frameon=True, shadow=True)

    # ---------- Ajustes finais ----------
    for ax in axes:
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_facecolor('#fafafa')

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()
