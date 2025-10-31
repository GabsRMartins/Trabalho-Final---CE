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
        return self.peso / (self.altura ** 2)
    
    def calcular_tmb(self) -> float:
        
        if self.sexo.lower() == 'm':
            return 88.362 + (13.397 * self.peso) + (4.799 * self.altura * 100) - (5.677 * self.idade)
        else:
            return 447.593 + (9.247 * self.peso) + (3.098 * self.altura * 100) - (4.330 * self.idade)

    def calcular_gasto_calorico_total(self) -> float:
        tmb = self.calcular_tmb()
        return (tmb * self.nivel_atividade) + self.gasto_treino