from typing import List, Tuple
import random
from pulp import *
from src.entities.alimento import AlimentoItem

# Cache global para armazenar a melhor solução anterior (elitismo)
_melhor_solucao_cache = {
    'alimentos': None,
    'score': -float('inf'),
    'calorias': 0,
    'peso_execucoes': 0  # Quantas execuções sem mudança
}

# Cache para armazenar histórico de dietas (máximo 10)
_historico_dietas = []

class IndividuoGenetico:
    """Representa um indivíduo da população no algoritmo genético"""
    def __init__(self, cromossomo: List[int], alimentos: List[AlimentoItem], meta_calorica: float):
        self.cromossomo = cromossomo  # Lista de 0s e 1s indicando presença/ausência
        self.alimentos = alimentos
        self.meta_calorica = meta_calorica
        self.fitness = 0
        self.calcular_fitness()
    
    def calcular_fitness(self):
        """Calcula o fitness (qualidade) deste indivíduo"""
        alimentos_selecionados = [self.alimentos[i] for i in range(len(self.alimentos)) 
                                 if self.cromossomo[i] == 1]
        
        if len(alimentos_selecionados) == 0:
            self.fitness = -1000
            return
        
        calorias_total = sum(a.calorias for a in alimentos_selecionados)
        
        # Penalidade por desvio calórico
        desvio_calorico = abs(calorias_total - self.meta_calorica)
        penalidade_calorica = max(0, desvio_calorico - (self.meta_calorica * 0.1))
        
        # Pontuação nutricional
        pontuacao_nutricional = sum(calcular_pontuacao_nutricional(a, self.meta_calorica) 
                                   for a in alimentos_selecionados)
        
        # Bônus por variedade (5-7 alimentos idealmente)
        num_alimentos = len(alimentos_selecionados)
        bonus_variedade = 10 if 5 <= num_alimentos <= 7 else max(0, 5 - abs(num_alimentos - 6))
        
        # Verificar balanceamento por categoria
        bonus_balanceamento = verificar_balanceamento_categorias(alimentos_selecionados)
        
        # Fitness final
        self.fitness = pontuacao_nutricional + bonus_variedade + bonus_balanceamento - (penalidade_calorica / 100)
    
    def mutar(self, taxa_mutacao: float = 0.1):
        """Aplica mutação aleatória no cromossomo"""
        for i in range(len(self.cromossomo)):
            if random.random() < taxa_mutacao:
                self.cromossomo[i] = 1 - self.cromossomo[i]
        self.calcular_fitness()
    
    def cruzar(self, outro: 'IndividuoGenetico') -> Tuple['IndividuoGenetico', 'IndividuoGenetico']:
        """Realiza cruzamento (crossover) com outro indivíduo"""
        ponto_corte = random.randint(1, len(self.cromossomo) - 1)
        
        novo_cromo1 = self.cromossomo[:ponto_corte] + outro.cromossomo[ponto_corte:]
        novo_cromo2 = outro.cromossomo[:ponto_corte] + self.cromossomo[ponto_corte:]
        
        filho1 = IndividuoGenetico(novo_cromo1, self.alimentos, self.meta_calorica)
        filho2 = IndividuoGenetico(novo_cromo2, self.alimentos, self.meta_calorica)
        
        return filho1, filho2

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

def obter_categoria_alimento(nome: str) -> str:
    """Obtém a categoria de um alimento"""
    categorias = {
        'proteinas': ['frango', 'ovo', 'peixe', 'carne', 'leite', 'queijo'],
        'carboidratos': ['arroz', 'batata', 'quinoa', 'aveia', 'pão'],
        'leguminosas': ['feijão', 'lentilha', 'grão'],
        'vegetais': ['brócolis', 'espinafre', 'cenoura'],
        'frutas': ['banana', 'maçã', 'laranja', 'abacate'],
        'gorduras': ['azeite', 'castanha', 'amendoim']
    }
    
    nome_lower = nome.lower()
    for categoria, alimentos in categorias.items():
        if any(alim in nome_lower for alim in alimentos):
            return categoria
    return 'outro'

def verificar_balanceamento_categorias(alimentos: List[AlimentoItem]) -> float:
    """Verifica se há balanceamento entre categorias de alimentos"""
    categorias = {
        'proteinas': 0,
        'carboidratos': 0,
        'leguminosas': 0,
        'vegetais': 0,
        'frutas': 0,
        'gorduras': 0,
    }
    
    for alimento in alimentos:
        categoria = obter_categoria_alimento(alimento.nome)
        if categoria in categorias:
            categorias[categoria] += 1
    
    # Verificar presença mínima de categorias importantes
    bonus = 0
    if categorias['proteinas'] >= 1:
        bonus += 15
    if categorias['carboidratos'] >= 1:
        bonus += 15
    if categorias['vegetais'] >= 1:
        bonus += 10
    if categorias['frutas'] >= 1:
        bonus += 5
    
    # Penalidade por excesso de uma única categoria
    max_categoria = max(categorias.values())
    if max_categoria > 2:
        bonus -= (max_categoria - 2) * 5
    
    return bonus

def mochila_alimentos(alimentos: List[AlimentoItem], capacidade_calorica: float, usar_elitismo: bool = True) -> List[AlimentoItem]:
    """Otimiza a seleção de alimentos usando algoritmo genético com elitismo"""
    global _melhor_solucao_cache
    

    variacao = random.uniform(-2, 2)
    capacidade_calorica = max(1500, min(3500, capacidade_calorica + variacao))
    
    # ====== ALGORITMO GENÉTICO ======
    tamanho_populacao = 50
    geracoes = 30
    taxa_mutacao = 0.08 
    taxa_elitismo_ga = 0.15  
    
    # Inicializa população aleatória
    populacao = []
    for _ in range(tamanho_populacao):
        cromossomo = [random.randint(0, 1) for _ in range(len(alimentos))]
        individuo = IndividuoGenetico(cromossomo, alimentos, capacidade_calorica)
        populacao.append(individuo)
    
    # Evolui a população
    for geracao in range(geracoes):
        # Ordena por fitness
        populacao.sort(key=lambda x: x.fitness, reverse=True)
        
        # Elitismo: mantém os melhores
        num_elite = max(1, int(tamanho_populacao * taxa_elitismo_ga))
        nova_populacao = [IndividuoGenetico(ind.cromossomo.copy(), alimentos, capacidade_calorica) 
                         for ind in populacao[:num_elite]]
        
        # Gera nova população por cruzamento e mutação
        while len(nova_populacao) < tamanho_populacao:
            # Seleção por torneio
            pai1 = _torneio_selecao(populacao, tamanho_torneio=3)
            pai2 = _torneio_selecao(populacao, tamanho_torneio=3)
            
            # Cruzamento
            filho1, filho2 = pai1.cruzar(pai2)
            
            # Mutação
            if random.random() < taxa_mutacao:
                filho1.mutar(taxa_mutacao)
            if random.random() < taxa_mutacao:
                filho2.mutar(taxa_mutacao)
            
            nova_populacao.append(filho1)
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)
        
        populacao = nova_populacao[:tamanho_populacao]
    
    # Obtém a melhor solução
    populacao.sort(key=lambda x: x.fitness, reverse=True)
    melhor_individuo = populacao[0]
    
    selecionados = [alimentos[i] for i in range(len(alimentos)) 
                   if melhor_individuo.cromossomo[i] == 1]
    
    calorias_total = sum(a.calorias for a in selecionados)
    score_atual = melhor_individuo.fitness
    
    # ====== IMPLEMENTAÇÃO DE ELITISMO MULTI-EXECUÇÃO ======
    if usar_elitismo and _melhor_solucao_cache['alimentos'] is not None:
        melhor_score = _melhor_solucao_cache['score']
        peso_execucoes = _melhor_solucao_cache['peso_execucoes']
        
        prob_elite = min(0.90, 0.50 + (peso_execucoes * 0.20))
        
        # Se a solução atual é 2% pior, mantenha a anterior com muito alta probabilidade
        if score_atual < melhor_score * 0.98:
            if random.random() < prob_elite:
                selecionados = _melhor_solucao_cache['alimentos'].copy()
                calorias_total = _melhor_solucao_cache['calorias']
                score_atual = melhor_score
                _melhor_solucao_cache['peso_execucoes'] += 1
            else:
                _melhor_solucao_cache['peso_execucoes'] = max(0, _melhor_solucao_cache['peso_execucoes'] - 1)
        else:
            # Solução atual é melhor
            _melhor_solucao_cache['alimentos'] = selecionados.copy()
            _melhor_solucao_cache['score'] = score_atual
            _melhor_solucao_cache['calorias'] = calorias_total
            _melhor_solucao_cache['peso_execucoes'] = 0
    else:
        # Primeira execução
        _melhor_solucao_cache['alimentos'] = selecionados.copy()
        _melhor_solucao_cache['score'] = score_atual
        _melhor_solucao_cache['calorias'] = calorias_total
        _melhor_solucao_cache['peso_execucoes'] = 0
    
    calorias_total = sum(a.calorias for a in selecionados)
    if not (capacidade_calorica * 0.90 <= calorias_total <= capacidade_calorica * 1.10):
        alimentos_nao_selecionados = [a for a in alimentos if a not in selecionados]
        
        if calorias_total < capacidade_calorica * 0.90:
            alimentos_nao_selecionados.sort(key=lambda x: x.calorias)
            for alimento in alimentos_nao_selecionados:
                if calorias_total + alimento.calorias <= capacidade_calorica * 1.10:
                    selecionados.append(alimento)
                    calorias_total += alimento.calorias
                if calorias_total >= capacidade_calorica * 0.90:
                    break
        
        elif calorias_total > capacidade_calorica * 1.10:
            selecionados.sort(key=lambda x: x.calorias, reverse=True)
            while calorias_total > capacidade_calorica * 1.10 and len(selecionados) > 4:
                removed = selecionados.pop(0)
                calorias_total -= removed.calorias
    

    calorias_final = sum(a.calorias for a in selecionados)
    adicionar_dieta_historico(selecionados, calorias_final)
    
    return selecionados

def _torneio_selecao(populacao: List[IndividuoGenetico], tamanho_torneio: int = 3) -> IndividuoGenetico:
    torneio = random.sample(populacao, min(tamanho_torneio, len(populacao)))
    return max(torneio, key=lambda x: x.fitness)


def resetar_cache_elitismo():
    global _melhor_solucao_cache, _historico_dietas
    _melhor_solucao_cache = {
        'alimentos': None,
        'score': -float('inf'),
        'calorias': 0,
        'peso_execucoes': 0
    }
    _historico_dietas = []

def obter_historico_dietas() -> List[dict]:

    global _historico_dietas
    return _historico_dietas.copy()

def adicionar_dieta_historico(alimentos: List[AlimentoItem], calorias: float):

    global _historico_dietas
    

    id_dieta = tuple(sorted([a.nome for a in alimentos]))
    

    for dieta in _historico_dietas:
        if dieta['id'] == id_dieta:
            return
    

    _historico_dietas.append({
        'id': id_dieta,
        'alimentos': alimentos.copy(),
        'calorias': calorias
    })
    
    # Manter apenas as 10 mais recentes
    if len(_historico_dietas) > 10:
        _historico_dietas.pop(0)