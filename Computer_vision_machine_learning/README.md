### README

# Análise de Machine Learning em Pokémons

Este projeto foi desenvolvido como parte da disciplina de Visão Computacional do curso de Engenharia da Computação na Universidade Católica Dom Bosco. O objetivo é explorar técnicas de machine learning utilizando Pokémons como dados de entrada.

## Título do Trabalho
Análise de Machine Learning em Pokémons

## Nome do Aluno
Raphael Victor

## Professor
Hemerson Pistori

## Data
28 de maio de 2024

## Introdução
Este experimento utiliza Pokémons como dados para análise de machine learning. Os Pokémons foram escolhidos devido à diversidade de tipos e características únicas que cada tipo possui, facilitando a criação de um conjunto de dados rico e variado.

## Metodologia
- **Tipos de Pokémons Utilizados:** Água, Grama, Fogo, Dragão, Fada e Sombrio.
- **Gerações de Pokémons:** Foram utilizados Pokémons da 1ª à 7ª geração para o treinamento e da 8ª e 9ª geração para os experimentos.
- **Hyperparâmetros Ajustados:** Número de epochs, batch size e learning rate.

## Experimentos
Os experimentos envolveram ajustes nos hiperparâmetros para observar os efeitos sobre a performance do modelo. A seguir estão alguns pontos-chave dos experimentos realizados:

1. **Epochs:** Inicialmente, foram utilizados 30 epochs. Aumentamos as epochs para melhorar a acurácia.
2. **Batch Size:** Aumentamos o batch size para observar melhorias na performance.
3. **Learning Rate:** Modificamos o learning rate em diferentes experimentos para analisar seu impacto.

## Resultados
- **Overfitting:** Observamos que o modelo apresentava overfitting, ajustando-se muito bem aos dados de treinamento, mas não generalizando bem para dados de validação.
- **Acurácia por Classe:** O modelo teve um desempenho muito bom para a classe "FOGO" (100% de acurácia), desempenho razoável para "GRAMA", "FADA" e "SOMBRIO", mas dificuldades significativas com "ÁGUA" e "DRAGÃO".

## Conclusões
O estudo concluiu que o modelo de machine learning tem dificuldade em capturar subtipos de Pokémons não explícitos. A melhor performance foi obtida ao aumentar epochs e learning rate, mas ainda há muito espaço para melhorias.

## Próximos Passos
Para melhorar os resultados, sugerimos:
- Aumentar o batch size.
- Diminuir o número de epochs em alguns casos.
- Aumentar o learning rate.

Este projeto serviu como uma base divertida e educativa para explorar técnicas de machine learning utilizando um conjunto de dados não convencional.

## Contato
Para mais informações sobre este projeto, entre em contato com Raphael Victor.

## Agradecimentos
Agradecemos ao professor Hemerson Pistori pela orientação e suporte ao longo do desenvolvimento deste projeto.