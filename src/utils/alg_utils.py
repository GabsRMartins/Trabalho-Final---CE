from typing import List
import random
from pulp import *
from src.entities.alimento import AlimentoItem

def calcular_pontuacao_nutricional(alimento: AlimentoItem, meta_calorica: float) -> float:
    """Calcula a pontuação nutricional de um alimento baseado em seus atributos"""
    # Categorias de alimentos
    categorias = {
        'proteinas': ['frango', 'ovo', 'peixe', 'carne', 'leite', 'queijo'],
        'carboidratos': ['arroz', 'batata', 'quinoa', 'aveia', 'pão'],
        'leguminosas': ['feijão', 'lentilha', 'grão'],
        'vegetais': ['brócolis', 'espinafre', 'cenoura'],
        'frutas': ['banana', 'maçã', 'laranja', 'abacate'],
        'gorduras': ['azeite', 'castanha', 'amendoim']
    }
    
    # Pontuação base
    pontuacao = 1.0
    nome_lower = alimento.nome.lower()
    
    # Pontuação por categoria
    for categoria, alimentos in categorias.items():
        if any(alim in nome_lower for alim in alimentos):
            if categoria == 'proteinas':
                pontuacao *= 1.4  # Proteínas são essenciais
            elif categoria == 'carboidratos':
                pontuacao *= 1.3  # Carboidratos para energia
            elif categoria == 'leguminosas':
                pontuacao *= 1.35  # Boa fonte de proteína e fibras
            elif categoria == 'vegetais':
                pontuacao *= 1.25  # Vitaminas e minerais
            elif categoria == 'frutas':
                pontuacao *= 1.2   # Vitaminas e fibras
            elif categoria == 'gorduras':
                pontuacao *= 1.15  # Gorduras boas, mas em menor quantidade
            
    # Ajuste pela proporção calórica ideal
    calorias_ideais_refeicao = meta_calorica / 3  # Divide em 3 refeições
    if abs(alimento.calorias - calorias_ideais_refeicao) <= 100:
        pontuacao *= 1.2  # Bônus para porções adequadas
    elif alimento.calorias > calorias_ideais_refeicao * 1.5:
        pontuacao *= 0.8  # Penalidade para alimentos muito calóricos
        
    return pontuacao

def mochila_alimentos(alimentos: List[AlimentoItem], capacidade_calorica: float) -> List[AlimentoItem]:
    """Otimiza a seleção de alimentos usando PuLP para uma dieta balanceada"""
    # Variação suave na capacidade calórica
    variacao = random.uniform(-25, 25)  # Reduzida para ±25 kcal
    capacidade_calorica = max(1500, min(3500, capacidade_calorica + variacao))
    
    # Criar o problema de otimização
    prob = LpProblem("Dieta_Otimizada", LpMaximize)
    
    # Variáveis de decisão (0 ou 1 para cada alimento)
    escolhas = LpVariable.dicts("Escolha",
                              ((alimento.nome) for alimento in alimentos),
                              0, 1, LpInteger)
    
    # Pontuações nutricionais
    pontuacoes = {alimento.nome: calcular_pontuacao_nutricional(alimento, capacidade_calorica)
                 for alimento in alimentos}
    
    # Função objetivo
    prob += lpSum([escolhas[alimento.nome] * pontuacoes[alimento.nome] for alimento in alimentos])
    
    # Restrições de calorias mais precisas
    prob += lpSum([escolhas[alimento.nome] * alimento.calorias for alimento in alimentos]) <= capacidade_calorica * 1.05
    prob += lpSum([escolhas[alimento.nome] * alimento.calorias for alimento in alimentos]) >= capacidade_calorica * 0.95
    
    # Restrição de variedade total (5-7 alimentos)
    prob += lpSum([escolhas[alimento.nome] for alimento in alimentos]) >= 5
    prob += lpSum([escolhas[alimento.nome] for alimento in alimentos]) <= 7
    # Restrições por categoria de alimento
    categorias = {
        'proteinas': ['frango', 'ovo', 'peixe', 'carne', 'leite', 'queijo'],
        'carboidratos': ['arroz', 'batata', 'quinoa', 'aveia', 'pão'],
        'leguminosas': ['feijão', 'lentilha', 'grão'],
        'vegetais': ['brócolis', 'espinafre', 'cenoura'],
        'frutas': ['banana', 'maçã', 'laranja', 'abacate'],
        'gorduras': ['azeite', 'castanha', 'amendoim']
    }
    
    # Adicionar restrições por categoria
    for categoria, palavras_chave in categorias.items():
        alimentos_categoria = [alimento.nome for alimento in alimentos 
                             if any(palavra in alimento.nome.lower() for palavra in palavras_chave)]
        if alimentos_categoria:
            if categoria == 'proteinas':
                prob += lpSum([escolhas[nome] for nome in alimentos_categoria]) >= 1  # Pelo menos 1 proteína
            elif categoria == 'carboidratos':
                prob += lpSum([escolhas[nome] for nome in alimentos_categoria]) >= 1  # Pelo menos 1 carboidrato
            elif categoria == 'leguminosas':
                prob += lpSum([escolhas[nome] for nome in alimentos_categoria]) >= 1  # Pelo menos 1 leguminosa
            elif categoria == 'vegetais':
                prob += lpSum([escolhas[nome] for nome in alimentos_categoria]) >= 1  # Pelo menos 1 vegetal
            elif categoria == 'frutas':
                prob += lpSum([escolhas[nome] for nome in alimentos_categoria]) <= 2  # Máximo 2 frutas
            elif categoria == 'gorduras':
                prob += lpSum([escolhas[nome] for nome in alimentos_categoria]) <= 1  # Máximo 1 gordura
    
    # Resolver o problema
    prob.solve(PULP_CBC_CMD(msg=False))
    
    # Recuperar os alimentos selecionados
    selecionados = []
    for alimento in alimentos:
        if escolhas[alimento.nome].value() and escolhas[alimento.nome].value() > 0.5:
            selecionados.append(alimento)
    
    # Ajuste fino de calorias se necessário
    calorias_total = sum(alimento.calorias for alimento in selecionados)
    if not (capacidade_calorica * 0.95 <= calorias_total <= capacidade_calorica * 1.05):
        # Tentar ajustar com alimentos de baixa caloria primeiro
        alimentos_ordenados = sorted(
            [a for a in alimentos if a not in selecionados],
            key=lambda x: x.calorias
        )
        
        if calorias_total < capacidade_calorica * 0.95:
            # Adicionar alimentos até atingir o mínimo
            for alimento in alimentos_ordenados:
                if calorias_total + alimento.calorias <= capacidade_calorica * 1.05:
                    selecionados.append(alimento)
                    calorias_total += alimento.calorias
                if calorias_total >= capacidade_calorica * 0.95:
                    break
        
        elif calorias_total > capacidade_calorica * 1.05:
            # Remover alimentos mais calóricos até ficar dentro do limite
            selecionados.sort(key=lambda x: x.calorias, reverse=True)
            while calorias_total > capacidade_calorica * 1.05 and len(selecionados) > 5:
                removed = selecionados.pop(0)
                calorias_total -= removed.calorias
    
    return selecionados