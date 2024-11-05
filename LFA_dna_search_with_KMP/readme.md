# DNA Sequence Search Tool

Este projeto implementa uma ferramenta para buscar subsequências de DNA em uma sequência maior, utilizando dois algoritmos de busca: **busca básica** e **KMP (Knuth-Morris-Pratt)**. A interface gráfica facilita a inserção das sequências e apresenta os resultados, incluindo uma visualização detalhada do processo do algoritmo KMP.

## Dependências

Para rodar este projeto, você precisará ter instalado:

- Python 3.x
- Tkinter (para interface gráfica)

Se você não tiver o `Tkinter`, pode instalá-lo com o seguinte comando (caso esteja em um ambiente baseado em Linux):

```bash
sudo apt-get install python3-tk
```

## Resumo do Código

### Arquivo `gui.py`
Este arquivo contém a lógica da interface gráfica utilizando o `Tkinter`. Ele permite ao usuário:

1. Inserir uma sequência de DNA e uma subsequência.
2. Verificar se as sequências contêm apenas os caracteres "C", "T", "A" e "G".
3. Realizar a busca da subsequência utilizando tanto o algoritmo de **busca básica** quanto o **KMP**.
4. Visualizar os resultados, que incluem as posições encontradas e o número de comparações feitas por cada algoritmo.
5. Visualizar passo a passo a execução do algoritmo KMP.

### Arquivo `kmp.py`
Este arquivo implementa o algoritmo KMP (Knuth-Morris-Pratt) para buscar uma subsequência dentro de uma sequência maior. Ele inclui:

1. Uma função `compute_lps_array` que calcula o array LPS (Longest Prefix Suffix) utilizado pelo algoritmo KMP.
2. A função `kmp_search` que executa a busca, retornando as posições encontradas e o número de comparações feitas.

### Arquivo `comparation.py`
Este arquivo contém a implementação do algoritmo de busca básica para encontrar uma subsequência dentro de uma sequência maior de DNA. A busca é feita de maneira simples e direta, comparando cada caractere da subsequência com uma parte correspondente da sequência de DNA.

1. Função `basic_search` o algoritmo percorre cada posição possível da sequência de DNA onde a subsequência pode se encaixar.


## Como Utilizar

1. Clone este repositório ou baixe os arquivos.
2. Execute o arquivo `gui.py` com Python:
   ```bash
   python3 gui.py
   ```
3. Insira a sequência de DNA ou insira uma sequência pré-pronta de um arquivo .txt e a subsequência que deseja buscar. Ambas devem conter apenas os caracteres "C", "T", "A", "G".
4. Clique no botão **Search** para realizar a busca.
5. O resultado será mostrado na interface, incluindo as posições das ocorrências e o número de comparações feitas pelos dois algoritmos.
6. Uma visualização passo a passo do algoritmo KMP será mostrada na parte inferior da janela.

## Agradecimentos

Este projeto foi desenvolvido como parte do curso de Engenharia de Computação, 6º semestre, por:

- **Aluno**: Raphael Victor de Araujo Alencar
- **Professor**: Hemerson Pistori

