# Busca a cadeia "aba" dentro de um arquivo de texto
# Exemplo de uso:
# $ python busca_v1.py -c aba -f exemplo_maior.txt

# Lê os parâmetros passados na linha de comando
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

# Criando o autômato KMP para buscar a palavra "aba"
alfabeto=['a','b']
estados=['s0','s1','s2','s3']
inicial=['s0']
finais=['s3']
transicoes=[
   ['s0','a','s1'],
   ['s0','b','s0'],
   ['s1','a','s1'],
   ['s1','b','s2'],
   ['s2','a','s3'],
   ['s2','b','s0'],
   ['s3','a','s1'],
   ['s3','b','s2']
]

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
   print('Estado atual = ',estado)
   print('Simbolo atual = ',simbolo)
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
import matplotlib.pyplot as plt

# Cria um grafo vazio
G = nx.DiGraph()

# Coloca os vértices no grafo G
G.add_nodes_from(estados)

# Colocar as arestas no grafo G
for v in transicoes:
   G.add_edge(v[0],v[2],label=v[1])
   
# Visualizando o grafo usando networkx
# Note os problemas com laços e arestas múltiplas
pos=nx.spring_layout(G)
nx.draw_networkx(G, pos, with_labels = True)
nx.draw_networkx_edge_labels(G, pos = pos, edge_labels=nx.get_edge_attributes(G, 'label'),label_pos=0.5)

plt.show()


  
