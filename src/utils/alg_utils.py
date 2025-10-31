from typing import List, Tuple
import random
from src.entities.alimento import AlimentoItem

def calcular_pontuacao_nutricional(alimento: AlimentoItem, meta_calorica: float) -> float:
    # Pontuação base pela proximidade à meta
    pontuacao = 1.0 - abs(alimento.calorias - meta_calorica/3) / meta_calorica
    
    # Bônus para proteínas (assumindo que carnes, ovos, leite têm mais proteína)
    if any(palavra in alimento.nome.lower() for palavra in ['frango', 'ovo', 'leite']):
        pontuacao *= 1.3
    
    # Bônus para alimentos com nutrientes essenciais
    if any(palavra in alimento.nome.lower() for palavra in ['feijão', 'arroz', 'banana', 'maçã']):
        pontuacao *= 1.2
        
    return pontuacao

def mochila_alimentos(alimentos: List[AlimentoItem], capacidade_calorica: float) -> List[AlimentoItem]:
    # Adiciona variação à capacidade calórica alvo
    variacao = random.uniform(-50, 50)
    capacidade_calorica = max(1200, capacidade_calorica + variacao)
    
    n = len(alimentos)
    # Matriz dp agora armazena tuplas (valor, variedade)
    dp = [[(0, 0) for _ in range(int(capacidade_calorica) + 1)] for _ in range(n + 1)]
    keep = [[False for _ in range(int(capacidade_calorica) + 1)] for _ in range(n + 1)]
    
    # Embaralha alimentos para adicionar variação
    alimentos_disponiveis = alimentos.copy()
    random.shuffle(alimentos_disponiveis)
    
    for i in range(1, n + 1):
        alimento = alimentos_disponiveis[i-1]
        pontuacao = calcular_pontuacao_nutricional(alimento, capacidade_calorica)
        
        for w in range(int(capacidade_calorica) + 1):
            if alimento.calorias <= w:
                # Calcula valor incluindo variedade nutricional
                valor_atual = pontuacao + dp[i-1][w-alimento.calorias][0]
                variedade = dp[i-1][w-alimento.calorias][1] + 1
                
                if valor_atual > dp[i-1][w][0]:
                    dp[i][w] = (valor_atual, variedade)
                    keep[i][w] = True
                else:
                    dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = dp[i-1][w]
    
    # Recupera os alimentos selecionados
    selecionados = []
    i, w = n, int(capacidade_calorica)
    calorias_total = 0
    
    while i > 0 and len(selecionados) < 8:  # Limite máximo de 8 alimentos por refeição
        if keep[i][w] and calorias_total < capacidade_calorica:
            alimento = alimentos_disponiveis[i-1]
            # Adiciona alguma aleatoriedade na seleção
            if random.random() < 0.8:  # 80% de chance de selecionar
                selecionados.append(alimento)
                calorias_total += alimento.calorias
                w -= alimento.calorias
        i -= 1
    
    # Se não atingiu calorias suficientes, tenta adicionar mais alguns alimentos
    if calorias_total < capacidade_calorica * 0.8:
        alimentos_restantes = [a for a in alimentos if a not in selecionados]
        while alimentos_restantes and calorias_total < capacidade_calorica:
            alimento = random.choice(alimentos_restantes)
            if calorias_total + alimento.calorias <= capacidade_calorica * 1.1:
                selecionados.append(alimento)
                calorias_total += alimento.calorias
            alimentos_restantes.remove(alimento)
    
    return selecionados