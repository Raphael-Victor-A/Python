"""
Name Server - Servidor de Nomes Pyro4
Execute este script primeiro para iniciar o servidor de nomes

Comando: python nameserver.py
"""

import Pyro4
import sys
from Pyro4 import naming 
import time

def start_nameserver():
    try:
        print("=" * 60)
        print("INICIANDO NAME SERVER PYRO4")
        print("=" * 60)
        
        # Método alternativo
        ns = naming.startNS(host="localhost", port=9090)
        print("✓ Name Server iniciado em localhost:9090")
        print("Pressione Ctrl+C para parar\n")
        
        # Mantém o servidor rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nParando Name Server...")
            ns.close()
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    start_nameserver()