from typing import List

import numpy as np
from src.utils.graph_utils import plotar_evolucao

from src.entities.alimento import AlimentoItem
from src.entities.treino import FichaTreino

from src.entities.individuo import Individuo
from src.service.simulation import simular_evolucao




def criar_cardapio() -> List[AlimentoItem]:   
    """Cria uma lista diversificada de alimentos com suas calorias por 100g"""   
    return [
        # Proteínas
        AlimentoItem("Frango Grelhado", 165, 100),  # Proteína magra
        AlimentoItem("Ovo", 155, 100),              # Proteína completa
        AlimentoItem("Peixe", 206, 100),            # Ômega-3
        AlimentoItem("Carne Magra", 213, 100),      # Ferro
        
        # Carboidratos complexos
        AlimentoItem("Arroz Integral", 130, 100),   # Fibras
        AlimentoItem("Batata Doce", 86, 100),       # Vitamina A
        AlimentoItem("Quinoa", 120, 100),           # Proteína vegetal
        AlimentoItem("Aveia", 389, 100),            # Fibras
        
        # Leguminosas
        AlimentoItem("Feijão Preto", 77, 100),      # Ferro
        AlimentoItem("Lentilha", 116, 100),         # Proteína vegetal
        AlimentoItem("Grão de Bico", 164, 100),     # Fibras
        
        # Vegetais
        AlimentoItem("Brócolis", 55, 100),          # Vitamina C
        AlimentoItem("Espinafre", 23, 100),         # Ferro
        AlimentoItem("Cenoura", 41, 100),           # Vitamina A
        
        # Frutas
        AlimentoItem("Banana", 89, 100),            # Potássio
        AlimentoItem("Maçã", 52, 100),              # Fibras
        AlimentoItem("Laranja", 47, 100),           # Vitamina C
        AlimentoItem("Abacate", 160, 100),          # Gorduras saudáveis
        
        # Gorduras saudáveis
        AlimentoItem("Azeite", 884, 100),           # Ômega-9
        AlimentoItem("Castanha", 553, 100),         # Ômega-3
        AlimentoItem("Amendoim", 567, 100),         # Proteína
        
        # Laticínios
        AlimentoItem("Leite Desnatado", 42, 100),   # Cálcio
        AlimentoItem("Iogurte", 59, 100),           # Probióticos
        AlimentoItem("Queijo Branco", 264, 100),    # Proteína
    ]

def criar_exemplo_individuo() -> Individuo:
    """Cria um exemplo de indivíduo para simulação"""
    return Individuo(
        peso=75.0,           # 75 kg
        altura=1.75,         # 1.75 m
        idade=30,            # 30 anos
        sexo='m',           # masculino
        nivel_atividade=1.5, # moderadamente ativo
        gasto_treino=400,    # 400 kcal gastas no treino
        taxa_gordura=25.0    # 25% de gordura corporal
    )

if __name__ == "__main__":
    # Criar lista de alimentos disponíveis
    alimentos = criar_cardapio()
    
    # Criar indivíduo para simulação
    individuo = criar_exemplo_individuo()
    
    # Criar ficha de treino (escolha entre "ABC", "ABCD" ou "PPL")
    ficha_treino = FichaTreino(tipo_divisao="ABC")
    
    print("=== Estado Inicial ===")
    print(f"Peso: {individuo.peso:.1f} kg")
    print(f"IMC: {individuo.calcular_imc():.1f}")
    print(f"Taxa de Gordura: {individuo.taxa_gordura:.1f}%")
    print(f"Gasto Calórico Total: {individuo.calcular_gasto_calorico_total():.0f} kcal")
    print(f"\nGasto Calórico com Treino (semanal): {ficha_treino.calcular_gasto_semanal(individuo.peso):.0f} kcal")
    print(f"Gasto Calórico Médio Diário (treino): {ficha_treino.calcular_gasto_diario_medio(individuo.peso):.0f} kcal")
    
    print("\n" + str(ficha_treino))
    print("\nIniciando simulação de 36 semanas...")
    
    # Simular evolução por 36 semanas
    simular_evolucao(individuo, alimentos, ficha_treino, 36)
    
    print("\n=== Estado Final ===")
    print(f"Peso: {individuo.peso:.1f} kg")
    print(f"IMC: {individuo.calcular_imc():.1f}")
    print(f"Taxa de Gordura: {individuo.taxa_gordura:.1f}%")
    print(f"Gasto Calórico Total: {individuo.calcular_gasto_calorico_total():.0f} kcal")
    
    # Plotar resultados
    plotar_evolucao(individuo)
