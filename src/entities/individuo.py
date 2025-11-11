class Individuo:
    def __init__(self, peso: float, altura: float, idade: int, sexo: str, 
                 nivel_atividade: float, gasto_treino: int, taxa_gordura: float):
        self.peso = peso
        self.altura = altura
        self.idade = idade
        self.sexo = sexo
        self.nivel_atividade = nivel_atividade
        self.gasto_treino = gasto_treino
        self.taxa_gordura = taxa_gordura
        self.historico_imc = []
        self.historico_calorias = []
        self.historico_gordura = []
    
    def calcular_imc(self) -> float:
        """
        Calcula o Índice de Massa Corporal (IMC)
        
        Fórmula: IMC = peso(kg) / altura(m)²
        
        Fonte: WHO (1995) - Physical Status: The Use and Interpretation of Anthropometry
        https://www.ncbi.nlm.nih.gov/pubmed/8897289
        
        Classificação:
        - Abaixo do peso: < 18.5
        - Normal: 18.5 - 24.9
        - Sobrepeso: 25.0 - 29.9
        - Obesidade: ≥ 30.0
        """
        return self.peso / (self.altura ** 2)
    
    def calcular_tmb(self) -> float:
        """
        Calcula a Taxa Metabólica Basal (TMB) usando a Fórmula de Harris-Benedict (1919)
        
        Fórmula para Homens:
            TMB = 88.362 + (13.397 × peso_kg) + (4.799 × altura_cm) - (5.677 × idade_anos)
        
        Fórmula para Mulheres:
            TMB = 447.593 + (9.247 × peso_kg) + (3.098 × altura_cm) - (4.330 × idade_anos)
        
        Fontes:
        - Harris, J.A., & Benedict, F.G. (1919). "A Biometric Study of Human Basal Metabolism"
        - Refórmula de Roza & Shizgal (1984) com ajustes modernos
        
        TMB = energia gasta em repouso completo (em kcal/dia)
        """
        
        if self.sexo.lower() == 'm':
            return 88.362 + (13.397 * self.peso) + (4.799 * self.altura * 100) - (5.677 * self.idade)
        else:
            return 447.593 + (9.247 * self.peso) + (3.098 * self.altura * 100) - (4.330 * self.idade)

    def calcular_gasto_calorico_total(self) -> float:
        """
        Calcula o Gasto Energético Diário Total (TDEE - Total Daily Energy Expenditure)
        
        Fórmula: TDEE = TMB × Fator de Atividade + Gasto Treino
        
        Fatores de Atividade (Mifflin-St Jeor modificado):
        - 1.2: Sedentário (pouco exercício)
        - 1.375: Levemente ativo (1-3 dias/semana)
        - 1.55: Moderadamente ativo (3-5 dias/semana) ← USADO NESTA SIMULAÇÃO
        - 1.725: Muito ativo (6-7 dias/semana)
        - 1.9: Extremamente ativo (treina 2x/dia)
        
        Fontes:
        - Mifflin, M.D., et al. (1990). "A new predictive equation for resting energy expenditure"
          American Journal of Clinical Nutrition, 51(2): 241-247
        - ACSM Guidelines
        
        Returns:
            Gasto calórico diário total em kcal
        """
        tmb = self.calcular_tmb()
        return (tmb * self.nivel_atividade) + self.gasto_treino