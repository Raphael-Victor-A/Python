# core.py
import random

class CFGGenerator:
    def __init__(self, grammar):
        self.grammar = grammar

    def generate(self, symbol='S', max_depth=10):
        # Controla a profundidade da recursão para evitar loops infinitos
        if max_depth == 0:
            return ""
        
        if symbol not in self.grammar:
            return symbol  # Retorna o símbolo literal se não for um não-terminal

        # Escolhe uma produção aleatória
        production = random.choice(self.grammar[symbol])
        result = []

        for token in production.split():
            # Permite que as regras sejam aplicadas recursivamente
            result.append(self.generate(token, max_depth - 1))

        return ' '.join(result)

    def generate_infinite_text(self, symbol='S', sentence_count=5, max_depth=10):
        # Gera várias frases concatenadas para simular um texto "infinito"
        text = []
        for _ in range(sentence_count):
            text.append(self.generate(symbol, max_depth))
        return '. '.join(text) + '.'

    def set_grammar(self, new_grammar):
        self.grammar = new_grammar
