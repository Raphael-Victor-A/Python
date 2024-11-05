Esboço de código em python para rodar autômatos
de estados finitos determinístico para busca

v1: autômato fixo que busca a palavra "aba" dentro de um
texto cujo alfabeto é {a,b}.
v2: cria um autômato no estilo do KMP a partir da
palavra a ser buscada

Testado com

- Ubuntu 22.04
- conda 23.3.1
- python 3.11.3

Autor: Hemerson Pistori (pistori@ucdb.br)

------------------------------------------------------
Preparar o ambiente e instalar dependências. 
------------------------------------------------------
Comando úteis:
$ conda create -n lfa
$ conda env list
$ conda activate lfa
$ conda install networkx matplotlib
$ pip install pyvis==0.3.1
$ conda list
  Remove tudo para instalar de novo:
$ conda remove --name lfa --all

------------------------------------------------------
Executar o código para buscar a palavra "aba" no
arquivo exemplo_maior.txt
------------------------------------------------------
Comandos úteis:
$ conda activate lfa
$ python --version
$ python busca_v1.py -c aba -f exemplo_maior.txt

------------------------------------------------------
Resultados esperados
------------------------------------------------------
- Mostrará na tela a imagem original juntamente com
  as imagens com ruído, suavizada e bordas
- Salvará as imagens resultantes em disco na
  mesma pasta que a imagem original mas com nome
  modificado 
  
------------------------------------------------------
Alguns comandos úteis do terminal Linux (BASH)
------------------------------------------------------
# Procura na pasta atual (".") e em todas as sub-pastas
# os arquivos cujo nome começam com "bus" e terminam
# com ".zip"
$ find . -iname "bus*.zip"

# Cria uma pasta chamda softwareLFA dentro da pasta
# em que você se encontra no momento (que é representada
# sempre pelo ponto "."). 
$ mkdir ./programasLFA

# Mostra a pasta atual
$ pwd

# Lista o conteúdo da pasta atual
$ ls

# Entra na pasta programasLFA
# Use TAB para completar os comandos sem precisar
# digitar tudo
$ cd programasLFA 

# Move um arquivo de uma pasta para outra
# Os ".." indicam a pasta pai, ou a pasta que
# contém a pasta em que você está agora.
$ mv ../Downloads/buscaPalavra.zip .

# Descompacta o .zip
$ unzip buscaPalavra.zip 

# Entra na pasta descompactada 
$ cd buscaPalavra

# Mostra o conteúdo de um arquivo txt
$ more README.txt
ou
$ cat README.txt

# Abre um editor simples para editar o arquivo
# o "&" serve para liberar o terminal para continuar
# sendo usado.
$ gedit README.txt &
ou para ver o programa em python
$ gedit busca.py &



 
