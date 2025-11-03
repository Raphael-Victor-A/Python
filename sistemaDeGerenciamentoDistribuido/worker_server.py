"""
Worker Server - Servidor de Processamento de Tarefas
Este servidor processa tarefas enviadas pelo cliente

Comando: python worker_server.py [nome_do_worker]
Exemplo: python worker_server.py Servidor1
"""

import Pyro4
import sys
import time
import random
from datetime import datetime

@Pyro4.expose
class TaskWorker:
    """Classe que representa um servidor worker que processa tarefas"""
    
    def __init__(self, worker_name):
        self.worker_name = worker_name
        self.tasks_completed = 0
        print(f"\n[{worker_name}] Worker inicializado e pronto para receber tarefas")
    
    def calculate_factorial(self, n):
        """Calcula o fatorial de um número"""
        try:
            print(f"\n[{self.worker_name}] Recebendo tarefa: Calcular fatorial de {n}")
            
            if n < 0:
                raise ValueError("Número deve ser não-negativo")
            
            # Simula processamento (remove para calcular mais rápido)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Calcula o fatorial
            result = 1
            for i in range(2, n + 1):
                result *= i
            
            self.tasks_completed += 1
            
            print(f"[{self.worker_name}] ✓ Fatorial({n}) = {result} | Tarefas completadas: {self.tasks_completed}")
            
            return {
                'worker': self.worker_name,
                'task': f'factorial({n})',
                'input': n,
                'result': result,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_tasks': self.tasks_completed
            }
            
        except Exception as e:
            print(f"[{self.worker_name}] ✗ Erro ao processar fatorial({n}): {e}")
            raise e
    
    def sort_list(self, data):
        """Ordena uma lista de números"""
        try:
            print(f"\n[{self.worker_name}] Recebendo tarefa: Ordenar lista com {len(data)} elementos")
            
            # Simula processamento
            time.sleep(random.uniform(0.8, 2.0))
            
            # Ordena a lista
            sorted_data = sorted(data)
            
            self.tasks_completed += 1
            
            print(f"[{self.worker_name}] ✓ Lista ordenada com sucesso | Tarefas completadas: {self.tasks_completed}")
            
            return {
                'worker': self.worker_name,
                'task': f'sort_list(size={len(data)})',
                'input_size': len(data),
                'result': sorted_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_tasks': self.tasks_completed
            }
            
        except Exception as e:
            print(f"[{self.worker_name}] ✗ Erro ao ordenar lista: {e}")
            raise e
    
    def calculate_sum(self, numbers):
        """Calcula a soma de uma lista de números"""
        try:
            print(f"\n[{self.worker_name}] Recebendo tarefa: Calcular soma de {len(numbers)} números")
            
            # Simula processamento
            time.sleep(random.uniform(0.3, 1.0))
            
            # Calcula a soma
            total = sum(numbers)
            
            self.tasks_completed += 1
            
            print(f"[{self.worker_name}] ✓ Soma = {total} | Tarefas completadas: {self.tasks_completed}")
            
            return {
                'worker': self.worker_name,
                'task': f'sum({len(numbers)} numbers)',
                'input_size': len(numbers),
                'result': total,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_tasks': self.tasks_completed
            }
            
        except Exception as e:
            print(f"[{self.worker_name}] ✗ Erro ao calcular soma: {e}")
            raise e
    
    def get_statistics(self):
        """Retorna estatísticas do worker"""
        return {
            'worker': self.worker_name,
            'tasks_completed': self.tasks_completed
        }

def start_worker(worker_name):
    """Inicia um worker e o registra no Name Server"""
    try:
        # Cria o worker
        worker = TaskWorker(worker_name)
        
        # Cria o daemon Pyro
        daemon = Pyro4.Daemon()
        
        # Conecta ao Name Server
        print("🔍 Conectando ao Name Server...")
        ns = Pyro4.locateNS(host="localhost", port=9090)
        print("✓ Conectado ao Name Server")
        
        # Registra o worker
        uri = daemon.register(worker)
        ns.register(f"worker.{worker_name}", uri)
        
        print(f"✓ Worker registrado como: worker.{worker_name}")
        print(f"✓ URI: {uri}")
        
        # Lista workers registrados para verificação
        workers = ns.list(prefix="worker.")
        print(f"📋 Workers registrados: {list(workers.keys())}")
        
        print("\n" + "=" * 60)
        print(f"SERVIDOR WORKER '{worker_name}' INICIADO")
        print("=" * 60)
        print("Aguardando tarefas do cliente...")
        
        # Loop principal
        daemon.requestLoop()
        
    except Exception as e:
        print(f"✗ Erro ao iniciar worker: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Obtém o nome do worker dos argumentos ou usa um padrão
    if len(sys.argv) > 1:
        worker_name = sys.argv[1]
    else:
        worker_name = f"Servidor{random.randint(1, 999)}"
        print(f"Nenhum nome fornecido. Usando nome padrão: {worker_name}")
    
    start_worker(worker_name)