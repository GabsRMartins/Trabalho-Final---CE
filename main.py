import numpy as np
from typing import List, Tuple
import random
from utils.graph_utils import plotar_evolucao

from entities.alimento import AlimentoItem
from entities.individuo import Individuo

from utils.alg_utils import mochila_alimentos

def simular_evolucao(individuo: Individuo, alimentos: List[AlimentoItem], semanas: int):
    for semana in range(semanas):
        imc_atual = individuo.calcular_imc()
        gasto_calorico = individuo.calcular_gasto_calorico_total()
        
        
        if imc_atual < 18.5: 
            meta_calorica = gasto_calorico + 500
        elif imc_atual > 25: 
            meta_calorica = max(1200, gasto_calorico - 500)
        else:  
            meta_calorica = gasto_calorico

        
        selecao_alimentos = mochila_alimentos(alimentos, meta_calorica)
        calorias_totais = sum(item.calorias for item in selecao_alimentos)
        
       
        diferenca_calorica = calorias_totais - gasto_calorico
       
        mudanca_peso = diferenca_calorica / 7700
        individuo.peso += mudanca_peso
        
        
        individuo.historico_imc.append(individuo.calcular_imc())
        individuo.historico_calorias.append(calorias_totais)

from utils.graph_utils import plotar_evolucao


if __name__ == "__main__":
   
    alimentos = [
        AlimentoItem("Arroz", 130, 100),
        AlimentoItem("Feijão", 77, 100),
        AlimentoItem("Frango", 165, 100),
        AlimentoItem("Batata", 77, 100),
        AlimentoItem("Azeite", 884, 100),
        AlimentoItem("Pão", 265, 100),
        AlimentoItem("Banana", 89, 100),
        AlimentoItem("Leite", 42, 100),
        AlimentoItem("Ovo", 155, 100),
        AlimentoItem("Maçã", 52, 100)
    ]
    
    # Criar indivíduo exemplo
    individuo = Individuo(
        peso=70,          
        altura=1.75,      
        idade=25,        
        sexo='m',         
        nivel_atividade=1.5,  
        gasto_treino=400  
    )
    
    # Simular evolução por 12 semanas
    simular_evolucao(individuo, alimentos, 12)
    
    # Plotar resultados
    plotar_evolucao(individuo)