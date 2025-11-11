"""
Módulo de validações para a interface
Centraliza todas as validações de dados do formulário
"""

class ValidadorDados:
    """Classe responsável por validar dados pessoais"""
    
    @staticmethod
    def validar_peso(peso_str: str) -> tuple[bool, str, float]:
        """
        Valida o peso informado
        
        Args:
            peso_str: String com o valor do peso
            
        Returns:
            tuple: (é_válido, mensagem_erro, valor_peso)
        """
        try:
            peso = float(peso_str)
            if peso < 30 or peso > 300:
                return False, "Peso deve estar entre 30 e 300 kg", 0.0
            return True, "", peso
        except ValueError:
            return False, "Peso deve ser um número válido", 0.0
    
    @staticmethod
    def validar_altura(altura_str: str) -> tuple[bool, str, float]:
        """
        Valida a altura informada
        
        Args:
            altura_str: String com o valor da altura
            
        Returns:
            tuple: (é_válido, mensagem_erro, valor_altura)
        """
        try:
            altura = float(altura_str)
            if altura < 1.0 or altura > 2.3:
                return False, "Altura deve estar entre 1.0 e 2.3 m", 0.0
            return True, "", altura
        except ValueError:
            return False, "Altura deve ser um número válido", 0.0
    
    @staticmethod
    def validar_idade(idade_str: str) -> tuple[bool, str, int]:
        """
        Valida a idade informada
        
        Args:
            idade_str: String com o valor da idade
            
        Returns:
            tuple: (é_válido, mensagem_erro, valor_idade)
        """
        try:
            idade = int(idade_str)
            if idade < 15 or idade > 120:
                return False, "Idade deve estar entre 15 e 120 anos", 0
            return True, "", idade
        except ValueError:
            return False, "Idade deve ser um número inteiro válido", 0
    
    @staticmethod
    def validar_sexo(sexo: str) -> tuple[bool, str]:
        """
        Valida o sexo informado
        
        Args:
            sexo: String com o sexo (M ou F)
            
        Returns:
            tuple: (é_válido, mensagem_erro)
        """
        if not sexo:
            return False, "Selecione um sexo"
        if sexo.upper() not in ['M', 'F']:
            return False, "Sexo deve ser Masculino ou Feminino"
        return True, ""
    
    @staticmethod
    def validar_taxa_gordura(taxa_str: str) -> tuple[bool, str, float]:
        """
        Valida a taxa de gordura corporal informada
        
        Args:
            taxa_str: String com o valor da taxa de gordura
            
        Returns:
            tuple: (é_válido, mensagem_erro, valor_taxa)
        """
        try:
            taxa = float(taxa_str)
            if taxa < 3 or taxa > 60:
                return False, "Taxa de gordura deve estar entre 3 e 60%", 0.0
            return True, "", taxa
        except ValueError:
            return False, "Taxa de gordura deve ser um número válido", 0.0
    
    @staticmethod
    def validar_semanas(semanas_str: str) -> tuple[bool, str, int]:
        """
        Valida o número de semanas para simulação
        
        Args:
            semanas_str: String com o número de semanas
            
        Returns:
            tuple: (é_válido, mensagem_erro, valor_semanas)
        """
        try:
            semanas = int(semanas_str)
            if semanas < 1 or semanas > 208:  # Até 4 anos
                return False, "Número de semanas deve estar entre 1 e 208", 0
            return True, "", semanas
        except ValueError:
            return False, "Semanas deve ser um número inteiro válido", 0
    
    @staticmethod
    def validar_todos_dados(
        peso_str: str,
        altura_str: str,
        idade_str: str,
        sexo: str,
        taxa_gordura_str: str,
        semanas_str: str,
    ) -> tuple[bool, str, dict]:
        """
        Valida todos os dados de uma vez
        
        Args:
            peso_str: Peso em kg
            altura_str: Altura em metros
            idade_str: Idade em anos
            sexo: Sexo (M ou F)
            taxa_gordura_str: Taxa de gordura em %
            semanas_str: Número de semanas para simular
            
        Returns:
            tuple: (é_válido, mensagem_erro, dicionário_dados)
        """
        dados = {}
        mensagens_erro = []
        
        # Validar peso
        valido, msg, peso = ValidadorDados.validar_peso(peso_str)
        if not valido:
            mensagens_erro.append(msg)
        else:
            dados['peso'] = peso
        
        # Validar altura
        valido, msg, altura = ValidadorDados.validar_altura(altura_str)
        if not valido:
            mensagens_erro.append(msg)
        else:
            dados['altura'] = altura
        
        # Validar idade
        valido, msg, idade = ValidadorDados.validar_idade(idade_str)
        if not valido:
            mensagens_erro.append(msg)
        else:
            dados['idade'] = idade
        
        # Validar sexo
        valido, msg = ValidadorDados.validar_sexo(sexo)
        if not valido:
            mensagens_erro.append(msg)
        else:
            dados['sexo'] = sexo.lower()
        
        # Validar taxa de gordura
        valido, msg, taxa = ValidadorDados.validar_taxa_gordura(taxa_gordura_str)
        if not valido:
            mensagens_erro.append(msg)
        else:
            dados['taxa_gordura'] = taxa
        
        # Validar semanas
        valido, msg, semanas = ValidadorDados.validar_semanas(semanas_str)
        if not valido:
            mensagens_erro.append(msg)
        else:
            dados['semanas'] = semanas
        
        # Retornar resultado
        if mensagens_erro:
            return False, "\n".join(mensagens_erro), {}
        
        return True, "", dados


class FormularioHelper:
    """Classe auxiliar para formatação de mensagens de formulário"""
    
    @staticmethod
    def formatar_mensagem_sucesso(dados: dict) -> str:
        """Formata mensagem de sucesso com os dados validados"""
        return f"""Dados Validados com Sucesso!

Calculo:
• IMC: (será calculado pela entidade)
• TMB: (será calculado pela entidade)
• TDEE: (será calculado pela entidade)
• Massa Gorda: {(dados['peso'] * dados['taxa_gordura'] / 100):.1f} kg
• Massa Magra: {(dados['peso'] * (100 - dados['taxa_gordura']) / 100):.1f} kg

Proximo: Selecione uma Ficha de Treino"""
    
    @staticmethod
    def formatar_mensagem_erro(erros: str) -> str:
        """Formata mensagem de erro"""
        return f"Erro na validacao:\n{erros}"
