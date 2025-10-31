from typing import List
import random
from src.entities.individuo import Individuo
from src.entities.alimento import AlimentoItem
from src.utils.alg_utils import mochila_alimentos

def simular_evolucao(individuo: Individuo, alimentos: List[AlimentoItem], semanas: int):
    CALORIAS_POR_KG = 7700  # kcal por kg de gordura
    
    for semana in range(semanas):
        imc_atual = individuo.calcular_imc()
        gasto_calorico = individuo.calcular_gasto_calorico_total()
        
        # Define limites saudáveis de gordura corporal por sexo
        if individuo.sexo.lower() == 'm':
            gordura_min, gordura_max = 6, 24  # homens
        else:
            gordura_min, gordura_max = 16, 31  # mulheres

        # Cálculo do ajuste calórico
        ajuste_base = 0
        
        # Ajuste baseado no IMC (mais suave)
        if imc_atual > 25:
            ajuste_base -= 300 * min(2, (imc_atual - 25) / 5)  # Máximo -600 kcal
        elif imc_atual < 18.5:
            ajuste_base += 300 * min(2, (18.5 - imc_atual) / 3)  # Máximo +600 kcal
            
        # Ajuste baseado na taxa de gordura (mais suave)
        if individuo.taxa_gordura > gordura_max:
            ajuste_base -= 200 * min(2, (individuo.taxa_gordura - gordura_max) / 5)
        elif individuo.taxa_gordura < gordura_min:
            ajuste_base += 200 * min(2, (gordura_min - individuo.taxa_gordura) / 3)
        
        # Ajuste baseado na tendência (mais conservador)
        if len(individuo.historico_gordura) > 1:
            tendencia_gordura = individuo.taxa_gordura - individuo.historico_gordura[-1]
            if abs(tendencia_gordura) < 0.1:  # Mudança muito lenta
                ajuste_base *= 1.1  # Aumenta apenas 10%
        
        # Garante limites seguros de calorias
        meta_calorica = max(1500, min(3500, gasto_calorico + ajuste_base))
        
        # Variação diária menor (±50 kcal)
        variacao_diaria = random.uniform(-50, 50)
        meta_calorica += variacao_diaria

        # Seleciona alimentos e calcula calorias totais
        selecao_alimentos = mochila_alimentos(alimentos, meta_calorica)
        calorias_totais = sum(item.calorias for item in selecao_alimentos)
        
        # Calcula déficit/superávit calórico semanal
        diferenca_calorica_semanal = (calorias_totais - gasto_calorico) * 7
        
        # Mudança de peso semanal mais realista
        mudanca_peso = diferenca_calorica_semanal / CALORIAS_POR_KG
        novo_peso = max(45, min(150, individuo.peso + mudanca_peso))  # Limites seguros
        
        # Calcula mudança na composição corporal
        if diferenca_calorica_semanal < 0:
            # Em déficit: 75-85% da perda é gordura
            perc_gordura = random.uniform(0.75, 0.85)
        else:
            # Em superávit: 25-35% do ganho é gordura
            perc_gordura = random.uniform(0.25, 0.35)
        
        mudanca_massa_gordura = mudanca_peso * perc_gordura
        
        # Atualiza composição corporal
        massa_gordura_atual = individuo.peso * (individuo.taxa_gordura / 100)
        nova_massa_gordura = max(0, massa_gordura_atual + mudanca_massa_gordura)
        
        # Atualiza peso e taxa de gordura
        individuo.peso = novo_peso
        individuo.taxa_gordura = max(3, min(45, (nova_massa_gordura / novo_peso) * 100))
        
        # Registra histórico
        individuo.historico_imc.append(individuo.calcular_imc())
        individuo.historico_calorias.append(calorias_totais)
        individuo.historico_gordura.append(individuo.taxa_gordura)