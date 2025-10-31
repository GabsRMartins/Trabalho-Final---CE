from typing import List
import random
from src.entities.individuo import Individuo
from src.entities.alimento import AlimentoItem
from src.utils.alg_utils import mochila_alimentos

def simular_evolucao(individuo: Individuo, alimentos: List[AlimentoItem], semanas: int):
    for semana in range(semanas):
        imc_atual = individuo.calcular_imc()
        gasto_calorico = individuo.calcular_gasto_calorico_total()
        
        # Ajuste da meta calórica baseado no IMC e na taxa de gordura
        if individuo.sexo.lower() == 'm':
            gordura_min, gordura_max = 6, 24
        else:
            gordura_min, gordura_max = 16, 31

        # Cálculo do ajuste calórico baseado em múltiplos fatores
        ajuste_base = 0
        
        # Fator IMC
        if imc_atual > 25:
            ajuste_base -= 500 * (imc_atual - 25) / 5  # Aumenta déficit com maior IMC
        elif imc_atual < 18.5:
            ajuste_base += 500 * (18.5 - imc_atual) / 3  # Aumenta superávit com menor IMC
            
        # Fator Gordura
        if individuo.taxa_gordura > gordura_max:
            ajuste_base -= 300 * (individuo.taxa_gordura - gordura_max) / 5
        elif individuo.taxa_gordura < gordura_min:
            ajuste_base += 300 * (gordura_min - individuo.taxa_gordura) / 3
            
        # Fator Tendência (baseado no histórico)
        if len(individuo.historico_gordura) > 0:
            tendencia_gordura = individuo.taxa_gordura - individuo.historico_gordura[-1]
            if abs(tendencia_gordura) < 0.1:  # Se a mudança é muito lenta
                ajuste_base *= 1.2  # Aumenta o ajuste em 20%
        
        # Garante limites seguros
        meta_calorica = max(1200, min(4000, gasto_calorico + ajuste_base))
        
        # Adiciona aleatoriedade para simular variação diária (±100 kcal)
        variacao_diaria = random.uniform(-100, 100)
        meta_calorica += variacao_diaria

        # Seleciona alimentos e calcula calorias totais
        selecao_alimentos = mochila_alimentos(alimentos, meta_calorica)
        calorias_totais = sum(item.calorias for item in selecao_alimentos)
        
        # Calcula mudanças corporais
        diferenca_calorica = calorias_totais - gasto_calorico
        mudanca_peso = diferenca_calorica / 7700
        
        # Atualiza peso
        individuo.peso += mudanca_peso
        
        # Calcula mudança na gordura corporal de forma mais realista
        if diferenca_calorica < 0:
            # Em déficit, perde mais gordura (70-80%)
            perc_gordura = random.uniform(0.70, 0.80)
            mudanca_gordura = (diferenca_calorica / 7700) * perc_gordura
        else:
            # Em superávit, ganha menos gordura (20-30%)
            perc_gordura = random.uniform(0.20, 0.30)
            mudanca_gordura = (diferenca_calorica / 7700) * perc_gordura
        
        # Atualiza composição corporal
        massa_gordura = individuo.peso * (individuo.taxa_gordura / 100)
        nova_massa_gordura = massa_gordura + mudanca_gordura
        individuo.taxa_gordura = (nova_massa_gordura / individuo.peso) * 100
        
        # Registra histórico
        individuo.historico_imc.append(individuo.calcular_imc())
        individuo.historico_calorias.append(calorias_totais)
        individuo.historico_gordura.append(individuo.taxa_gordura)