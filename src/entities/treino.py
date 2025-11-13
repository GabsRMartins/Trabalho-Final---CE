from enum import Enum
from typing import List
from dataclasses import dataclass

class TipoTreino(Enum):
    """Estimativa de gasto calórico baseada no padrão MET (Metabolic Equivalent of Task).
    
    Fontes:
    - 2024 Compendium of Physical Activities (Ainsworth et al., 2024)
    - Journal of Sport and Health Science
    - Wikipedia: Metabolic Equivalent of Task
    
    Cálculo: kcal = (MET * 3.5 * peso_kg * duracao_minutos) / 200
    Baseado em: 1 MET = 1 kcal/kg/hora = 3.5 mL O2/kg/min
    
    NOTA: Valores reduzidos para estabilidade da simulação (usa ~50% do potencial máximo)
    """
    # Treinamento de força/resistência (valores conservadores)
    SUPERIOR = 3.0          # Musculação peito/costas/ombro (5-6 METs) → reduzido para estabilidade
    INFERIOR = 4.0          # Musculação pernas (7-9 METs) → reduzido para estabilidade
    PERNA_INTENSA = 4.5     # Agachamento pesado (9-10 METs) → reduzido para estabilidade
    
    # Cardio aeróbico (valores conservadores)
    CARDIO_LEVE = 2.5       # Caminhada leve (3-5 METs) → reduzido para estabilidade
    CARDIO_MODERADO = 3.75  # Corrida moderada (7-8 METs) → reduzido para estabilidade
    CARDIO_INTENSO = 5.0    # Corrida rápida (10-12 METs) → reduzido para estabilidade
    
    # Treinos mistos/funcionais (valores conservadores)
    FUNCIONAL = 4.25        # HIIT/Treino funcional (8-9 METs) → reduzido para estabilidade
    YOGA = 1.5              # Yoga com asanas (2.5-3.3 METs) → reduzido para estabilidade
    
    # Repouso/inativo
    REPOUSO = 1.0           # Dia de repouso/sedentário (1 MET)

@dataclass
class Exercicio:
    """Representa um exercício individual"""
    nome: str
    tipo_treino: TipoTreino
    series: int = 3
    repeticoes: int = 10
    
    def __repr__(self) -> str:
        return f"{self.nome} ({self.series}x{self.repeticoes})"

class FichaTreino:
    """Gerencia a ficha de treino de um indivíduo com divisão ABC (3 dias) ou ABCD (4 dias)
    
    Os valores de METs (Metabolic Equivalent of Task) são baseados em:
    - 2024 Compendium of Physical Activities
    - Ainsworth, B.E., et al. (2024). "2024 Adult Compendium of Physical Activities"
      Journal of Sport and Health Science, 13(1): 6-12
    - Wikipedia: Metabolic Equivalent of Task
    
    Cada tipo de treino tem um valor MET que representa quantas vezes o metabolismo em repouso
    é acelerado durante a atividade. O gasto calórico é calculado dinamicamente baseado no peso.
    """
    
    def __init__(self, tipo_divisao: str = "ABC"):
        """
        Inicializa a ficha de treino.
        tipo_divisao: "ABC" (3 dias), "ABCD" (4 dias) ou "PPL" (Push/Pull/Legs)
        """
        self.tipo_divisao = tipo_divisao
        self.treinos: dict = {}
        self._criar_ficha_padrao()
    
    def _criar_ficha_padrao(self):
        """Cria uma ficha de treino padrão baseada no tipo de divisão"""
        if self.tipo_divisao == "ABC":
            self.treinos = {
                'A': self._treino_superior(),  # Segunda
                'B': self._treino_inferior(),  # Terça
                'Repouso1': TipoTreino.REPOUSO,  # Quarta
                'C': self._treino_funcional(),  # Quinta
                'Repouso2': TipoTreino.REPOUSO,  # Sexta
                'Repouso3': TipoTreino.REPOUSO,  # Sábado
                'Repouso4': TipoTreino.REPOUSO,  # Domingo
            }
        elif self.tipo_divisao == "ABCD":
            self.treinos = {
                'A': self._treino_superior(),
                'B': self._treino_inferior(),
                'C': self._treino_funcional(),
                'D': self._treino_cardio_moderado(),
                'Repouso1': TipoTreino.REPOUSO,
                'Repouso2': TipoTreino.REPOUSO,
                'Repouso3': TipoTreino.REPOUSO,
            }
        elif self.tipo_divisao == "PPL":
            self.treinos = {
                'Push': self._treino_superior(),    # Peito, Ombro, Tríceps
                'Pull': self._treino_superior(),     # Costas, Bíceps
                'Legs': self._treino_perna_intensa(), # Pernas
                'Repouso1': TipoTreino.REPOUSO,
                'Repouso2': TipoTreino.REPOUSO,
                'Cardio': self._treino_cardio_leve(),
                'Repouso3': TipoTreino.REPOUSO,
            }
    
    def _treino_superior(self) -> TipoTreino:
        """Treino de membros superiores"""
        return TipoTreino.SUPERIOR
    
    def _treino_inferior(self) -> TipoTreino:
        """Treino de membros inferiores padrão"""
        return TipoTreino.INFERIOR
    
    def _treino_perna_intensa(self) -> TipoTreino:
        """Treino intenso de pernas"""
        return TipoTreino.PERNA_INTENSA
    
    def _treino_funcional(self) -> TipoTreino:
        """Treino funcional/HIIT"""
        return TipoTreino.FUNCIONAL
    
    def _treino_cardio_leve(self) -> TipoTreino:
        """Cardio leve"""
        return TipoTreino.CARDIO_LEVE
    
    def _treino_cardio_moderado(self) -> TipoTreino:
        """Cardio moderado"""
        return TipoTreino.CARDIO_MODERADO
    
    def calcular_gasto_semanal(self, peso: float, duracao_minutos: int = 60) -> float:
        """
        Calcula o gasto calórico total da semana
        
        Fórmula: kcal = (MET * 3.5 * peso_kg * duracao_minutos) / 200
        Baseado em: 1 MET = 1 kcal/kg/hora = 3.5 mL O2/kg/min
        
        Args:
            peso: Peso do indivíduo em kg
            duracao_minutos: Duração média de cada sessão (padrão 60 min)
            
        Returns:
            Gasto calórico semanal em kcal
        """
        gasto_total = 0
        for dia, tipo_treino in self.treinos.items():
            if isinstance(tipo_treino, TipoTreino):
                # Fórmula baseada em METs: kcal = (MET * 3.5 * peso * duracao) / 200
                gasto_dia = (tipo_treino.value * 3.5 * peso * duracao_minutos) / 200
                gasto_total += gasto_dia
        return gasto_total
    
    def calcular_gasto_diario_medio(self, peso: float) -> float:
        """
        Calcula o gasto calórico médio diário
        
        Args:
            peso: Peso do indivíduo em kg
            
        Returns:
            Gasto calórico médio por dia em kcal
        """
        gasto_semanal = self.calcular_gasto_semanal(peso)
        return gasto_semanal / 7
    
    def obter_gasto_dia_semana(self, dia_semana: int, peso: float, duracao_minutos: int = 60) -> float:
        """
        Obtém o gasto calórico de um dia específico da semana
        
        Args:
            dia_semana: 0 (segunda) a 6 (domingo)
            peso: Peso do indivíduo em kg
            duracao_minutos: Duração da sessão em minutos (padrão 60 min)
            
        Returns:
            Gasto calórico do dia em kcal
        """
        dias = list(self.treinos.keys())
        if dia_semana < len(dias):
            tipo_treino = self.treinos[dias[dia_semana]]
            if isinstance(tipo_treino, TipoTreino):
                return (tipo_treino.value * 3.5 * peso * duracao_minutos) / 200
        return 0
    
    def __repr__(self) -> str:
        return f"FichaTreino({self.tipo_divisao})"
    
    def __str__(self) -> str:
        resultado = f"Ficha de Treino - Divisão {self.tipo_divisao}\n"
        resultado += "-" * 50 + "\n"
        for dia, tipo_treino in self.treinos.items():
            if isinstance(tipo_treino, TipoTreino):
                resultado += f"{dia:12s}: {tipo_treino.name:15s} ({tipo_treino.value} kcal/100kg)\n"
        return resultado
