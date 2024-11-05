import random

# Guarda a gramática em uma lista de listas (inicial)
gramatica = [
    ['S', 'S', 'e', 'S'],  # Exemplo de regra recursiva para texto "virtualmente infinito"
    ['S', 'NP', 'VP'],
    ['NP', 'Ana'],
    ['NP', 'João'],
    ['NP', 'Pedro'],
    ['VP', 'foi', 'para', 'Cidade'],
    ['Cidade', 'Cuiabá'],
    ['Cidade', 'Campo Grande'],
    ['Cidade', 'São Paulo'],
    ['Cidade', 'Roma'],
    ['Cidade', 'Lima'],
    ['Cidade', 'Nova York'],
    ['Cidade', 'Chapecó']
]

# Lista dos símbolos não terminais
naoTerminais = ['S', 'NP', 'VP', 'Cidade']

# Símbolo inicial da gramática
inicial = 'S'

# Gera uma lista com as opções para substituir um determinado símbolo não terminal
def opcoesLadoDireito(naoTerminal):
    return [x[1:] for x in gramatica if x[0] == naoTerminal]

# Expande os símbolos não terminais escolhendo aleatoriamente a regra de produção
def expande(arvore):
    for i in range(len(arvore)):
        if arvore[i] in naoTerminais:
            opcoes = opcoesLadoDireito(arvore[i])  # Obtém as opções
            if opcoes:  # Verifica se há opções disponíveis
                arvore[i] = random.choice(opcoes)  # Escolhe aleatoriamente uma opção
                expande(arvore[i])  # Recursão para expandir ainda mais
            else:
                raise ValueError(f"Não há regras de produção para o não terminal: {arvore[i]}")


# Mostra a cadeia representada na árvore de derivação
def mostraCadeia(arvore):
    resultado = ""
    if isinstance(arvore, list):
        for filho in arvore:
            resultado += mostraCadeia(filho)
    else:
        resultado += arvore + " "
    return resultado

# Função principal para gerar os textos (agora retorna o texto ao invés de printar)
def gerar_texto(quant):
    textos = []
    for i in range(quant):
        arvore = [inicial]
        expande(arvore)
        textos.append(mostraCadeia(arvore))
    return textos 

# Função para atualizar a gramática (essa função pode ser chamada pelo GUI)
def atualizar_gramatica(nova_gramatica):
    global gramatica  # Declare como global para que ela seja modificada globalmente
    gramatica = nova_gramatica
