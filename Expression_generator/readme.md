
---

# Gerador de Texto CLC/CFG

## Descrição

Este projeto é um gerador de texto, baseado em uma Gramática Livre de Contexto (GLC/CFG). Utilizando uma gramática definida pelo usuário, o programa gera textos "virtualmente infinitos" ao combinar regras gramaticais de forma aleatória e recursiva. O projeto é composto por um núcleo de geração de texto e uma interface gráfica para facilitar o uso.

## Funcionalidades

- **Configuração de Gramática**: Permite que o usuário defina uma gramática em JSON, com regras para estruturação de frases.
- **Geração de Texto**: Utiliza as regras gramaticais definidas para produzir frases e textos de forma aleatória e "infinita".
- **Interface Gráfica**: A aplicação possui uma GUI em Tkinter, onde o usuário pode carregar, editar e atualizar a gramática, além de visualizar o texto gerado.
- **Carregar Gramática de Arquivo**: O usuário pode importar gramáticas em formato JSON diretamente para a aplicação.

## Estrutura do Projeto

- `nucleo.py`: Arquivo principal que contém a classe `CFGGenerator`, responsável pela lógica de geração de texto. Ele aplica regras gramaticais de forma recursiva para gerar frases e textos complexos.
- `gui.py`: Interface gráfica construída em Tkinter. Permite ao usuário interagir facilmente com a aplicação, carregar gramáticas, atualizar regras e gerar textos.

## Como Utilizar

1. Execute o arquivo `gui.py` para abrir a interface gráfica.
2. Na interface, insira ou carregue uma gramática em formato JSON.
3. Clique em "Atualizar Gramática" para confirmar a nova gramática.
4. Clique em "Gerar Texto" para ver o resultado baseado nas regras definidas.
5. O texto gerado aparecerá no campo de saída, podendo ser salvo ou copiado.

## Exemplo de Gramática

```json
{
  "S": ["NP VP", "S S", "VP NP"],
  "NP": ["Det N", "N"],
  "VP": ["V NP", "V"],
  "Det": ["o", "a", "os", "as", "um", "uma", "uns", "umas"],
  "N": ["homem", "mulher", "crianca", "cachorro", "gato", "cidade", "livro"],
  "V": ["corre", "come", "fala", "le", "pula"],
  "Extras": ["com", "para", "e", "mas", "ou"]
}
```

## Dependências

- Python 3.x
- Tkinter (incluído na instalação padrão do Python)
  
## Como Executar

Para iniciar a aplicação, execute o seguinte comando:

```bash
python gui.py
```

## Contribuição

Contribuições são bem-vindas. Sinta-se à vontade para fazer um fork do projeto, abrir issues ou enviar pull requests.

---
