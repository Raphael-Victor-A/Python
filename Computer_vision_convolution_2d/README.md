# Núcleo de Convolução - Aplicação em Python

## Descrição

Este projeto implementa uma aplicação em Python para aplicar convoluções em imagens utilizando uma interface gráfica. A interface permite ao usuário carregar uma imagem, definir ou carregar um núcleo de convolução e visualizar a imagem processada em comparação com a imagem original.

## Funcionalidades

- Carregar uma imagem em tons de cinza.
- Aplicar um núcleo de convolução definido pelo usuário.
- Carregar um núcleo de convolução a partir de um arquivo de texto.
- Resetar a imagem para a original.
- Visualizar a imagem original e a imagem resultante da convolução lado a lado.

## Dependências

Este projeto requer as seguintes bibliotecas:

- `cv2` (OpenCV)
- `numpy`
- `tkinter`
- `PIL` (Pillow)

Você pode instalar as dependências necessárias com os seguintes comandos:

```sh
pip install opencv-python-headless numpy pillow
```

## Como Executar

1. **Clone o repositório** ou copie o código para um arquivo Python.

2. **Instale as dependências** listadas acima.

3. **Execute o script** Python:

```sh
python nome_do_arquivo.py
```

## Estrutura do Código

### `criar_interface()`

Esta função define e exibe a interface gráfica utilizando `tkinter`. Inclui dois `Canvas` para exibir a imagem original e a imagem resultante da convolução, além de entradas para definir o núcleo de convolução e botões para interagir com a aplicação.

### `processar_valores(nucleo=None)`

Esta função aplica a convolução na imagem usando o núcleo definido pelo usuário ou carregado de um arquivo.

### `selecionar_imagem()`

Esta função abre um diálogo para selecionar uma imagem em tons de cinza do sistema de arquivos.

### `atualizar_imagem()`

Esta função atualiza os `Canvas` da interface com a imagem original e a imagem processada.

### `reset_imagem()`

Esta função reseta a imagem processada para a imagem original.

### `carregar_nucleo()`

Esta função abre um diálogo para carregar um núcleo de convolução a partir de um arquivo de texto.

### `aplicar_convolucao(nucleo)`

Esta função aplica a convolução na imagem utilizando o núcleo fornecido. A convolução é aplicada pixel por pixel, calculando a soma ponderada dos pixels vizinhos de acordo com o núcleo.

## Exemplo de Arquivo de Núcleo

O arquivo de núcleo deve conter 9 valores separados por espaços ou novas linhas, representando uma matriz 3x3. Exemplo:

```
0 -1 0
-1 5 -1
0 -1 0
```

## Licença

Este projeto é de código aberto e está licenciado sob a licença MIT. Sinta-se à vontade para modificar e distribuir conforme necessário.

---

**Autor**: Raphael Victor
**Data**: Maio de 2024