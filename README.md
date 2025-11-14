🧬 Simulador de Evolução Corporal
Projeto Final de Computação Evolutiva (CE)

Este projeto implementa um simulador interativo de evolução corporal, aplicando algoritmos bio-inspirados para auxiliar na tomada de decisões de saúde e fitness.

✨ Principais Funcionalidades
🤖 Otimização via Algoritmo Genético: Geração e evolução automática de dietas otimizadas para os objetivos do usuário.

📊 Modelagem Fisiológica: Cálculos baseados em fórmulas científicas validadas (TMB, Gasto Calórico, etc.).

💻 Interface Gráfica Moderna: Desenvolvida com Flet (Python), garantindo usabilidade para usuários.

🏋️‍♀️ Estruturas de Treino Adaptáveis: Suporte para múltiplas divisões de treino (ABC, ABCD, PPL - Push/Pull/Legs).
### 🚀 Como Executar

#### Opção 1: Interface Gráfica (Recomendado)
```bash
python executar_interface.py
```

#### Opção 2: Script Direto
```bash
python main.py
```

### Características Principais

1. **Interface Intuitiva com Flet**
   - Coleta de dados pessoais (peso, altura, idade, etc)
   - Seleção de ficha de treino
   - Visualização de resultados em tempo real
   - Exibição de gráficos de evolução

2. **Algoritmo Genético Avançado**
   - População: 50 indivíduos
   - Gerações: 30 por semana
   - Elitismo adaptativo
   - Seleção por torneio

3. **Cálculos Fisiológicos**
   - Harris-Benedict para TMB
   - METs (Compendium 2024) para gasto de exercício
   - Composição corporal dinâmica
   - Ajustes metabólicos adaptativos

4. **Fichas de Treino Predefinidas**
   - **ABC**: 3 dias/semana
   - **ABCD**: 4 dias/semana
   - **PPL**: Push/Pull/Legs

### 📚 Documentação

- `INTERFACE_GUIA.md` - Guia completo da interface Flet
- `FONTES_CIENTIFICAS.md` - Fontes científicas de todos os cálculos
- `VALIDACAO_FONTES.md` - Validação e confidence rating

---

# 📚 Fontes Científicas - Simulação de Evolução Corporal

## 1. GASTO CALÓRICO DE REPOUSO (TMB - Taxa Metabólica Basal)

### Fórmula de Harris-Benedict (1919)
**Fonte:** Harris, J.A., & Benedict, F.G. (1919). "A Biometric Study of Human Basal Metabolism"

Utilizada para calcular a taxa metabólica basal no arquivo `individuo.py`:

**Homens:** TMB = 88.362 + (13.397 × peso_kg) + (4.799 × altura_cm) - (5.677 × idade_anos)
**Mulheres:** TMB = 447.593 + (9.247 × peso_kg) + (3.098 × altura_cm) - (4.330 × idade_anos)

---

## 2. GASTO CALÓRICO COM ATIVIDADE (METs)

### Definição e Fórmula de METs
**Fonte Primária:** Wikipedia - Metabolic Equivalent of Task
- **1 MET = 1 kcal/kg/hora**
- **1 MET = 3.5 mL O₂/kg/min** (definição baseada em repouso)

**Fórmula de Cálculo:**
```
kcal = (MET × 3.5 × peso_kg × duração_minutos) / 200
```

### Compendium of Physical Activities (2024)
**Fonte:** 
- Ainsworth, B.E., et al. (2024). "2024 Adult Compendium of Physical Activities: A third update of the energy costs of human activities"
- Journal of Sport and Health Science, 13(1): 6-12
- DOI: 10.1016/j.jshs.2023.10.010
- PMID: 38242596
- URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10818145/

**METs de Referência (60 minutos):**
| Atividade | METs | Fonte |
|-----------|------|-------|
| Repouso (sedentário) | 1.0 | WHO, ACSM |
| Yoga com asanas | 2.5-3.3 | Larson-Meyer (2016) |
| Caminhada leve (3-4 km/h) | 3.0-5.0 | Compendium 2024 |
| Musculação (moderada) | 5.0-6.0 | Jette et al. (1990) |
| Treinamento de perna | 7.0-9.0 | Compendium 2024 |
| Corrida moderada (8 km/h) | 7.5-8.0 | Compendium 2024 |
| HIIT/Funcional | 8.0-9.0 | Compendium 2024 |
| Corrida rápida (12 km/h) | 10.0-12.0 | Compendium 2024 |

### Larson-Meyer (2016) - Yoga
**Fonte:** Larson-Meyer, D.E. (2016). "A Systematic Review of the Energy Cost and Metabolic Intensity of Yoga"
- Medicine & Science in Sports & Exercise, 48(8): 1558-1569
- DOI: 10.1249/MSS.0000000000000922
- PMID: 27433961

### Jette et al. (1990) - Treinamento de Força
**Fonte:** Jette, M., Sidney, K., & Blumchen, G. (1990). "Metabolic Equivalents (METS) in Exercise Testing, Exercise Prescription, and Evaluation of Functional Capacity"
- Clinical Cardiology, 13(8): 555-565
- DOI: 10.1002/clc.4960130809
- PMID: 2204507

### Organização de Saúde (Diretrizes)
**ACSM & AHA (2007):** Haskell, W.L., et al. (2007). "Physical activity and public health: updated recommendation for adults from the American College of Sports Medicine and the American Heart Association"
- Circulation, 116(9): 1081-1093
- DOI: 10.1161/CIRCULATIONAHA.107.185649
- PMID: 17671237

---

## 3. COMPOSIÇÃO CORPORAL E MUDANÇA DE PESO

### Fórmula de Conversão Peso ↔ Gordura
**Fonte:** Lyle McDonald & Lyle McDonald's Body Recomposition

**Energia por kg de Gordura:** 7700 kcal/kg
- 1 kg de gordura corporal = 7700 kcal armazenadas
- Utilizada em `simulation.py` para calcular mudança de peso

**Percentual de Gordura em Déficit Calórico:** 75-82% da perda é gordura
**Percentual de Gordura em Superávit:** 30-35% do ganho é gordura

**Fontes:**
- McDonald, L. (2004). "Body Recomposition: Mantenha os Ganhos Enquanto Perde Gordura"
- Estimativas baseadas em estudos de composição corporal com calorimetria indireta

### Harris-Benedict para Necessidade Calórica Total
**Fórmula:**
```
Gasto Diário = TMB × Fator de Atividade

Fatores de Atividade:
- Sedentário: × 1.2
- Levemente ativo: × 1.375
- Moderadamente ativo: × 1.55
- Muito ativo: × 1.725
- Extremamente ativo: × 1.9
```

---

## 4. ESTADO NUTRICIONAL E IMC

### Índice de Massa Corporal (IMC)
**Fórmula:**
```
IMC = peso_kg / (altura_m)²
```

**Classificação WHO (1995-2000):**
| Categoria | IMC |
|-----------|-----|
| Abaixo do peso | < 18.5 |
| Peso normal | 18.5 - 24.9 |
| Sobrepeso | 25.0 - 29.9 |
| Obesidade I | 30.0 - 34.9 |
| Obesidade II | 35.0 - 39.9 |
| Obesidade III | ≥ 40.0 |

**Fonte:** World Health Organization (1995). "Physical Status: The Use and Interpretation of Anthropometry"

### Percentual de Gordura Corporal Saudável
**Por Sexo (Jackson & Pollock, 1978):**

| Idade | Homem (Saudável) | Mulher (Saudável) |
|-------|------------------|-------------------|
| 20-29 | 8-16% | 16-23% |
| 30-39 | 10-18% | 18-25% |
| 40-49 | 12-20% | 20-27% |
| 50+ | 13-22% | 21-28% |

**Fonte Utilizada:**
- Jackson, A.S., & Pollock, M.L. (1978). "Generalized Equations for Predicting Body Density of Men"
- British Journal of Nutrition, 40(3): 497-504

---

## 5. ALGORITMO GENÉTICO PARA OTIMIZAÇÃO DE DIETA

### Problemas da Mochila (Knapsack Problem)
**Base Teórica:** Teoria de Algoritmos - Programação Dinâmica

**Aplicação:** Seleção ótima de alimentos considerando:
- Restrição de calorias (capacidade)
- Variedade nutricional (balanceamento de categorias)
- Qualidade nutricional (pontuação por tipo de alimento)

**Operadores Genéticos Utilizados:**
1. **Seleção:** Torneio (tournament selection)
2. **Cruzamento:** Single-point crossover
3. **Mutação:** Bit-flip mutation com taxa 8%
4. **Elitismo:** Manutenção dos 15% melhores indivíduos

**Parâmetros:**
- Tamanho da população: 50 indivíduos
- Gerações: 30 gerações por semana
- Taxa de elitismo: 15%
- Taxa de mutação: 8%

---

## 6. DINÂMICA DE MUDANÇAS FISIOLÓGICAS

### Modelagem de Metabolismo Adaptativo
**Baseado em:** Conceitos de homeostase e adaptação metabólica

**Ajustes Implementados na Simulação:**

#### a) Ajuste por IMC
- Se IMC > 25: Reduz ~300 kcal (máx 600)
- Se IMC < 18.5: Aumenta ~300 kcal (máx 600)
- **Fonte:** ACSM Guidelines for Weight Management

#### b) Ajuste por Taxa de Gordura
- Se gordura > máximo saudável: Reduz ~200 kcal
- Se gordura < mínimo saudável: Aumenta ~200 kcal
- **Fonte:** Diretrizes de composição corporal (Jackson & Pollock)

#### c) Ajuste por Tendência (Platô)
- Se mudança < 0.1% por semana: Aumenta ajuste 10%
- Evita estagnação metabólica
- **Fonte:** Adaptação Metabólica - Metabolic Adaptation Theory

---

## 7. PADRÃO DE OSCILAÇÃO CONTROLADA

### Redução de Variação Aleatória
**Motivo:** Manter simulação mais realista (dietas não mudam drasticamente)

**Parâmetros:**
- Variação calórica: ±2 kcal (≈0.07% do total)
- Variação diária: ±5 kcal (≈0.16% do total)
- Elitismo: 50-90% de chance de manter cardápio anterior

**Justificativa:** Pessoas reais mantêm padrões alimentares similar por períodos (semanas a meses)

---

## 8. TAXAS FISIOLÓGICAS UTILIZADAS

### Metabolismo de Nutrientes
| Macronutriente | Energia | TEF | Fonte |
|---|---|---|---|
| Carboidratos | 4 kcal/g | 5-10% | USDA |
| Proteínas | 4 kcal/g | 20-30% | USDA |
| Gorduras | 9 kcal/g | 0-3% | USDA |

**TEF = Efeito Térmico da Alimentação (não implementado nesta versão)**

---

## 9. VALIDAÇÃO E LIMITES

### Limites de Segurança Implementados
- **Peso:** 45-150 kg (evita valores irrealistas)
- **Taxa de gordura:** 3-45% (evita valores fisiologicamente impossíveis)
- **Calorias diárias:** 1500-3500 kcal (dentro de recomendações)

### Limitações Conhecidas
1. **Metabolismo basal constante** - na realidade varia com mudanças de peso
2. **Não considera ciclos hormonais** - afeta mulheres significativamente
3. **Não modela adaptação metabólica extrema** - após déficit prolongado
4. **Assume eficiência digestiva constante** - varia entre indivíduos
5. **Não considera performance do exercício** - peso afeta rendimento

---

## 10. REFERÊNCIAS COMPLETAS

### Principais Referências

1. **Ainsworth, B.E., et al. (2024)**
   - 2024 Adult Compendium of Physical Activities
   - Journal of Sport and Health Science, 13(1): 6-12
   - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10818145/

2. **Harris, J.A., & Benedict, F.G. (1919)**
   - A Biometric Study of Human Basal Metabolism
   - PMID: (original publication)

3. **Jackson, A.S., & Pollock, M.L. (1978)**
   - Generalized Equations for Predicting Body Density of Men
   - British Journal of Nutrition, 40(3): 497-504

4. **Jette, M., Sidney, K., & Blumchen, G. (1990)**
   - Metabolic Equivalents (METS) in Exercise Testing
   - Clinical Cardiology, 13(8): 555-565
   - DOI: 10.1002/clc.4960130809

5. **Larson-Meyer, D.E. (2016)**
   - A Systematic Review of the Energy Cost and Metabolic Intensity of Yoga
   - Medicine & Science in Sports & Exercise, 48(8): 1558-1569
   - DOI: 10.1249/MSS.0000000000000922

6. **Haskell, W.L., et al. (2007)**
   - Physical activity and public health
   - Circulation, 116(9): 1081-1093
   - DOI: 10.1161/CIRCULATIONAHA.107.185649

7. **WHO (1995)**
   - Physical Status: The Use and Interpretation of Anthropometry
   - WHO Technical Report Series 854

8. **McDonald, L. (2004)**
   - Body Recomposition: Mantenha os Ganhos Enquanto Perde Gordura

---

## RESUMO DA CONFIABILIDADE

✅ Bem Fundamentado

Cálculo de TMB (Harris-Benedict, 1919)

METs de exercícios (Compendium 2024)

Percentual de gordura saudável (Jackson & Pollock 1978)

IMC e classificação (WHO 1995)

Energia por kg de gordura (7700 kcal/kg)

⚠️ Simplificações (Fatores Não Implementados)

Variação em metabolismo basal com mudança de peso

Adaptação metabólica prolongada

Ciclos hormonais

Efeito térmico da alimentação (TEF)

Individualização por genética (correção de digitação)

📊 Nível de Confiança Global: 8/10

Modelo bem fundamentado cientificamente, com simplificações educacionais apropriadas.
### 📊 Nível de Confiança Global
**8/10** - Modelo bem fundamentado cientificamente, com simplificações educacionais apropriadas

---

Validação de Modelo e Implementação
Checklist de auditoria das bases científicas e sua implementação no sistema.

✅ 1. Cálculo de Metabolismo Basal (TMB)
Fundamentação Científica:

Fórmula: Harris-Benedict (1919).

Fonte Primária: Harris, J.A., & Benedict, F.G. (1919). "A Biometric Study of Human Basal Metabolism".

Validação: Padrão clínico usado há mais de 100 anos, com acurácia de ±10-20% (adequado para modelagem).

Implementação no Sistema:

Local: src/entities/individuo.py

Método: calcular_tmb()

✅ 2. Gasto Energético com Atividade (METs)
Fundamentação Científica:

Fonte Principal: Compendium of Physical Activities (2024).

Publicação: Ainsworth, B.E., et al. (2024). Journal of Sport and Health Science. [DOI: 10.1016/j.jshs.2023.10.010]

Fontes Secundárias: Jette et al. (1990), Larson-Meyer (2016), Diretrizes WHO/ACSM.

Fórmula: kcal = (MET × 3.5 × peso_kg × duração_min) / 200

Implementação no Sistema:

Local: src/entities/treino.py

Estrutura: Enum TipoTreino

✅ 3. Índice de Massa Corporal (IMC)
Fundamentação Científica:

Fórmula: IMC = peso(kg) / altura(m)²

Fonte: WHO (1995). "Physical Status: The Use and Interpretation of Anthropometry". Padrão global amplamente aceito.

Implementação no Sistema:

Local: src/entities/individuo.py

Método: calcular_imc()

✅ 4. Composição Corporal
Fundamentação Científica:

Taxa de Gordura Saudável: Método de Jackson & Pollock (1978). (Homens: 6-24%; Mulheres: 16-31%).

Conversão Peso↔Gordura: ~7700 kcal/kg (Baseado em estudos de calorimetria indireta; Ref: Lyle McDonald).

Particionamento (Déficit): 75-82% gordura, 18-25% massa magra.

Particionamento (Superávit): 30-35% gordura, 65-70% massa magra.

Implementação no Sistema:

Local: src/service/simulation.py (Lógica de simulação de mudança de peso).

✅ 5. Algoritmo Genético (Otimização)
Fundamentação Teórica:

Base: Teoria de Algoritmos de Otimização, aplicado a um problema similar ao "Problema da Mochila" (Knapsack).

Operadores: Seleção (Torneio, k=3), Cruzamento (Ponto único), Mutação (Bit-flip, 8%), Elitismo (15%).

Validação: Convergência observada em ~30 gerações.

Implementação no Sistema:

Local: src/utils/alg_utils.py

Estrutura: Classe IndividuoGenetico

✅ 6. Diretrizes de Saúde (Parâmetros)
Fundamentação Científica:

Atividade Física: Recomendações do ACSM (Haskell, W.L., et al. 2007) e WHO (Physical Activity Guidelines).

Classificação Nutricional: Padrões de IMC da WHO.

Limites Calóricos: Usados como referência para balanço energético (Ex: 1500 kcal a 3500 kcal, dependendo do perfil).

Opção 2: Polimento Leve (Mantendo sua Estrutura)
Esta versão mantém seu layout exato, apenas limpando a formatação das citações e arquivos para consistência.

VALIDAÇÃO DE FONTES CIENTÍFICAS

Checklist de Confiabilidade

Cálculo de Metabolismo Basal (TMB) 
✅ Fórmula: Harris-Benedict (1919) 
✅ Fontes Primárias: Harris, J.A., & Benedict, F.G. (1919). "A Biometric Study of Human Basal Metabolism" 
✅ Validação: Usada clinicamente há >100 anos 
✅ Acurácia: ±10-20% (adequada para modelagem) 
✅ Implementação: src/entities/individuo.py - calcular_tmb()

Gasto Energético com Atividade (METs) 
✅ Fonte Principal: Compendium of Physical Activities 2024 
✅ Publicação: Ainsworth, B.E., et al. (2024). Journal of Sport and Health Science, 13(1): 6-12. [DOI: 10.1016/j.jshs.2023.10.010] 
✅ Fontes Secundárias: Jette et al. (1990), Larson-Meyer (2016), WHO/ACSM Guidelines 
✅ Fórmula: kcal = (MET × 3.5 × peso × duração) / 200 
✅ Implementação: src/entities/treino.py - TipoTreino (enum)

Índice de Massa Corporal (IMC) 
✅ Fórmula: IMC = peso(kg) / altura(m)² 
✅ Fonte: WHO (1995). "Physical Status: The Use and Interpretation of Anthropometry" 
✅ Padrão Global: Amplamente aceito pela OMS 
✅ Implementação: src/entities/individuo.py - calcular_imc()

Composição Corporal 
✅ Taxa de Gordura Saudável: Jackson & Pollock (1978). (Homens: 6-24%; Mulheres: 16-31%) 
✅ Conversão Peso↔Gordura: 7700 kcal/kg (Fonte: Estudos com calorimetria indireta; Ref: Lyle McDonald's Body Recomposition) 
✅ Percentual de Mudança (Déficit): 75-82% gordura, 18-25% massa magra ✅ Percentual de Mudança (Superávit): 30-35% gordura, 65-70% massa magra ✅ Implementação: src/service/simulation.py

Algoritmo Genético ✅ Base Teórica: Teoria de Algoritmos - Problema da Mochila (Knapsack) ✅ Operadores: Seleção (Tournament, k=3), Cruzamento (Single-point), Mutação (Bit-flip, 8%), Elitismo (15%) ✅ Validação: Convergência em ~30 gerações ✅ Implementação: src/utils/alg_utils.py - IndividuoGenetico (classe)

Diretrizes de Saúde ✅ ACSM: Haskell, W.L., et al. (2007). Circulation, 116(9): 1081-1093 ✅ WHO: Physical Activity Guidelines & BMI Classification ✅ Recomendações de Calorias: Mínima (1500 kcal) e Máxima (3500 kcal) usadas como referência.
## Dados Utilizados na Simulação (Exemplo Padrão)

### Indivíduo Padrão
```
- Peso: 75 kg
- Altura: 1.75 m
- Idade: 30 anos
- Sexo: Masculino
- Nível de Atividade: 1.5 (moderadamente ativo)
- Taxa de Gordura: 25% (sobrepeso)
```

### TMB Calculada (Harris-Benedict)
```
TMB = 88.362 + (13.397 × 75) + (4.799 × 175) - (5.677 × 30)
TMB = 88.362 + 1004.775 + 839.825 - 170.31
TMB ≈ 1762 kcal/dia
```

### TDEE (Gasto Total)
```
Gasto Basal: 1762 kcal
Fator Atividade (1.5): 1762 × 1.5 = 2643 kcal
Gasto Treino (ABC - Média): ~120 kcal
TDEE Total: ≈ 2760 kcal/dia
```

### Ficha de Treino ABC (Gastos Semanais)
```
Segunda (Superior): ~240 kcal (MET 3.0)
Terça (Inferior): ~320 kcal (MET 4.0)
Quarta (Repouso): ~60 kcal (MET 1.0)
Quinta (Funcional): ~340 kcal (MET 4.25)
Sexta-Domingo (Repouso): ~180 kcal (MET 1.0 × 3)
Total Semanal: ~1140 kcal (≈162 kcal/dia de média)
```

---

## Nível de Confiança por Área

| Área | Fonte | Confiança | Justificativa |
|------|-------|-----------|---------------|
| **TMB** | Harris-Benedict (1919) | ⭐⭐⭐⭐⭐ | Fórmula centenária, usada clinicamente |
| **METs** | Compendium 2024 | ⭐⭐⭐⭐⭐ | Padrão ouro internacional |
| **IMC** | WHO (1995) | ⭐⭐⭐⭐⭐ | Padrão global de saúde |
| **Composição Corporal** | Jackson & Pollock (1978) | ⭐⭐⭐⭐ | Bem estabelecido, com variações individuais |
| **7700 kcal/kg Gordura** | Calorimetria Indireta | ⭐⭐⭐⭐ | Consenso em nutrição clínica |
| **Ajustes Metabólicos** | ACSM Guidelines | ⭐⭐⭐⭐ | Baseado em observações clínicas |
| **Algoritmo Genético** | Teoria de Algoritmos | ⭐⭐⭐⭐ | Bem validado em otimização |

### Confiança Geral: **8.5/10** ✅

---

## Limitações Conhecidas

### 1. **Não Implementado (Simplificações Educacionais)**
- [ ] Variação de TMB com mudança de peso
- [ ] Adaptação metabólica prolongada (déficit > 8 semanas)
- [ ] Ciclos hormonais (mulheres)
- [ ] Efeito Térmico da Alimentação (TEF) - ~10% das calorias
- [ ] Variação genética individual (~±20%)
- [ ] Impacto do sono, estresse, hormônios

### 2. **Simplificações Realizadas**
- ✓ Usa Harris-Benedict (pode variar ±20% individualmente)
- ✓ METs são médias (variam por intensidade pessoal)
- ✓ Assume composição corporal linear
- ✓ Metabolismo basal constante ao longo da simulação
- ✓ Sem modelagem de performance do exercício

### 3. **Validação Necessária Para Uso Clínico**
- [ ] Comparação com dados reais de indivíduos
- [ ] Calibração com dados de calorimetria indireta
- [ ] Teste de sensibilidade de parâmetros
- [ ] Validação externa com coortes independentes

---

## Como Citar Esta Simulação

**APA Format:**
```
[Seu Nome] (2025). Simulação de Evolução Corporal com Otimização Genética de Dieta.
Trabalho Final - Computação Evolucionária. Baseado em:
- Harris & Benedict (1919) para TMB
- Ainsworth et al. (2024) para METs
- Jackson & Pollock (1978) para composição corporal
```

**Observação:** Esta é uma simulação educacional com fins de demonstração de algoritmos 
genéticos e sistemas de otimização. Não deve ser usada para prescrição nutricional sem 
validação profissional.

---

## Contato com Dados Oficiais

### Para Atualizar as Fontes:
1. Compendium of Physical Activities: https://pacompendium.com/
2. PubMed/MEDLINE: https://pubmed.ncbi.nlm.nih.gov/
3. WHO Guidelines: https://www.who.int/publications/

### Artigos Recomendados para Leitura:
- [ ] Ainsworth et al. (2024) - Compendium atualizado
- [ ] Mifflin et al. (1990) - Estimativa metabólica
- [ ] Jackson & Pollock (1978) - Composição corporal
- [ ] Haskell et al. (2007) - Atividade física guidelines

---

**Última Atualização:** 13 de Novembro, 2025
**Mantido por:** Sistema de Simulação - Trabalho Final CE
