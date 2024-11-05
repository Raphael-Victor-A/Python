# Busca a cadeia "aba" dentro de um arquivo de texto
# Exemplo de uso:
# $ python busca_v2.py -c aba -f exemplo_maior.txt

# Lê os parâmetros passados na linha de comando

# O autômato será desenhado no Browser (as vezes precisa dar F5 para visualizar)

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", default="entrada.txt",
                    help="Nome do arquivo onde buscar", metavar="FILE")
parser.add_argument("-c", "--cadeia",
                    help="Cadeia de caracteres a ser buscada")

args = parser.parse_args()

# Mostra os parâmetros lidos
print("Iniciando a busca SEM autômato")
print("Arquivo onde buscar:",args.file)
print("O quê deve ser buscado:",args.cadeia)

# Vou chamar de cadeia maior (cmaior) a cadeia
# que está dentro do arquivo 
cmaior=[]

# Abre o arquivo de entrada e lê uma letra por vez,
# linha por linha e vai colocando em um vetor
file = open(args.file, "r")
for linha in file:
    for letra in linha:
        if letra!='\n': cmaior.append(letra) 
print('Cadeia maior como vetor:')              
print(cmaior)

# Transforma a cadeia menor a ser buscada também
# em um vetor
cmenor = [char for char in args.cadeia]
print('Cadeia menor como vetor:')              
print(cmenor)

        
# Busca a cadeia menor dentro da cadeia maior
# usando um método não otimizado        
qtd_ocorrencias_sem=0
qtd_comparacoes_sem=0
for i in range(len(cmaior)):
  achou=True
  for j in range(len(cmenor)):
     if (i+j) == len(cmaior): 
         achou=False
         break
     qtd_comparacoes_sem = qtd_comparacoes_sem + 1 
     if cmenor[j] != cmaior[i+j]: achou=False
  if achou: 
     print('achou na posição',i)
     qtd_ocorrencias_sem=qtd_ocorrencias_sem+1
         
      
print("Iniciando a busca COM autômato")


# Cálcula o tamanho do maior prefixo que é igual
# a um sufixo da cadeia
def maiorPrefSufProprio(cadeia):
    maior=0
    # Usando o reserved pois quando achar o primeiro pode parar
    for i in reversed(range(len(cadeia)-1)):
        prefixo=cadeia[:(i+1)]
        sufixo=cadeia[-(i+1):]
        if prefixo==sufixo: 
           if len(prefixo) > maior:
              maior=len(prefixo)
              break
    return maior

# Cria todas as transicoes para o autômato KMP
def criaTransicoes(cadeia):
  sub=""
  estado=0
  transicoes=[]
  for estado in range(len(cadeia)+1):
    if estado < len(cadeia): letra_correta=cadeia[estado]
    else: letra_correta = 'FIM'
    for letra_alternativa in alfabeto:
      if letra_alternativa == letra_correta:
         proximo = estado+1
      else:
         proximo = maiorPrefSufProprio(sub+letra_alternativa)
      estado_antes = 's'+str(estado)
      estado_depois = 's'+str(proximo)
      transicao=[estado_antes,letra_alternativa,estado_depois]
      transicoes.append(transicao)
    estado=estado+1
    sub=sub+letra_correta
  return(transicoes)
  
# Criando o autômato KMP para buscar a palavra passada como parâmetro
cadeia=args.cadeia
total_estados=range(len(cadeia)+1)
alfabeto=['a','b']
estados=['s'+str(n) for n in total_estados]
inicial=estados[:1] 
finais=estados[-1:]
transicoes=criaTransicoes(cadeia)


# Aqui estou criando uma versão das transicoes
# usando um dicionário para deixar a busca
# pelo próximo estado mais eficiente
dtransicoes=dict(((e1,e2),s) for e1,e2,s in transicoes)

# Mostra na tela as partes do autômato
print('Alfabeto: ',alfabeto)
print('Estados: ',estados)
print('Estado inicial: ',inicial)
print('Estados finais: ',finais)
print('Transições: ',transicoes)
print('Transições como dicionário: ',dtransicoes)

# Percorre a cadeia de  entrada e
# executa o autômato
qtd_ocorrencias_com=0
qtd_comparacoes_com=0
estado=inicial[0]
for i in range(len(cmaior)):
   if estado in finais:
      print('Achou uma ocorrência na posicao ',i-len(cmenor))
      qtd_ocorrencias_com=qtd_ocorrencias_com+1      
   simbolo=cmaior[i]
   estado=dtransicoes[(estado,simbolo)]
   qtd_comparacoes_com=qtd_comparacoes_com+1
   
# Decide se a cadeia foi aceita ou não
# IMPORTANTE: Este autômato do exemplo
# faz um pouco mais do que apenas dizer
# se a cadeia é aceita ou não. Ele busca
# coisas dentro da cadeia   
if estado in finais:
   print('Achou uma ocorrência na posicao ',len(cmaior)-len(cmenor))
   qtd_ocorrencias_com=qtd_ocorrencias_com+1      
   print('Cadeia aceita')
else:
   print('Cadeia rejeitada') 

print('Quantidade de ocorrências SEM autômato = ',qtd_ocorrencias_sem)
print('Quantidade de comparações SEM autômato = ',qtd_comparacoes_sem)
print('Quantidade de ocorrências COM autômato = ',qtd_ocorrencias_com)
print('Quantidade de comparações COM autômato = ',qtd_comparacoes_com)
   
   
# Importa uma biblioteca que implementa um monte de funcionalidades
# para trabalhar com grafos (aqui neste exemplo vamos usar apenas
# para mostrar o autômato)
import networkx as nx 
#import matplotlib.pyplot as plt
from pyvis.network import Network

# Cria um grafo vazio
G = nx.DiGraph()

# Coloca os vértices no grafo G
G.add_nodes_from(estados)

# Colocar as arestas no grafo G
for v in transicoes:
   G.add_edge(v[0],v[2],label=v[1])
   
# Visualizando o grafo usando networkx e pyvis
nt = Network('500px', '800px', directed=True)
nt.from_nx(G)
nt.show('G.html', True)



  
