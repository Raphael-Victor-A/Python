"""
Cliente - Envia Várias Tarefas para um Servidor
Cenário 1: Um único cliente envia várias tarefas (cálculos) para um servidor

Comando: python client.py
"""

import Pyro4
import sys
import time
import random
from datetime import datetime

class TaskClient:
    """Cliente que envia tarefas para o servidor worker"""
    
    def __init__(self):
        try:
            # Conecta ao Name Server
            self.ns = Pyro4.locateNS(host="localhost", port=9090)
            print("=" * 60)
            print("CLIENTE DE TAREFAS - CENÁRIO 1")
            print("=" * 60)
            print("✓ Conectado ao Name Server\n")
        except Exception as e:
            print(f"✗ Erro ao conectar ao Name Server: {e}")
            print("\nCertifique-se de que o Name Server está rodando!")
            sys.exit(1)
    
    def get_worker(self):
        """Busca um worker disponível"""
        try:
            # Lista todos os workers registrados
            print("🔍 Buscando workers no Name Server...")
            workers = list(self.ns.list(prefix="worker.").items())
            
            print(f"📋 Workers encontrados: {len(workers)}")
            for name, uri in workers:
                print(f"   - {name} -> {uri}")
            
            if not workers:
                print("✗ Nenhum worker disponível no momento")
                return None
            
            # Pega o primeiro worker disponível
            worker_name, worker_uri = workers[0]
            
            print(f"✓ Conectando ao worker: {worker_name}")
            print(f"🔗 URI: {worker_uri}")
            
            # Cria o proxy para o worker
            worker = Pyro4.Proxy(worker_uri)
            
            # Testa a conexão
            print("🧪 Testando conexão com worker...")
            stats = worker.get_statistics()
            print(f"✅ Conexão OK! Worker: {stats['worker']}, Tarefas: {stats['tasks_completed']}")
            
            return worker, worker_name
            
        except Exception as e:
            print(f"✗ Erro ao buscar worker: {e}")
            return None
    
    def send_task(self, task_func, task_description):
        """Envia uma tarefa para o worker"""
        try:
            worker_info = self.get_worker()
            
            if not worker_info:
                return None
            
            worker, worker_name = worker_info
            
            print(f"\n{'─' * 60}")
            print(f"📤 ENVIANDO TAREFA: {task_description}")
            print(f"{'─' * 60}")
            
            # Executa a tarefa
            start_time = time.time()
            result = task_func(worker)
            end_time = time.time()
            
            # Exibe o resultado
            print(f"\n✅ TAREFA CONCLUÍDA")
            print(f"   Worker: {result['worker']}")
            print(f"   Resultado: {result['result']}")
            print(f"   Timestamp: {result['timestamp']}")
            print(f"   Tempo de processamento: {end_time - start_time:.2f}s")
            print(f"   Total de tarefas no worker: {result['total_tasks']}")
            
            return result
            
        except Exception as e:
            print(f"\n✗ ERRO ao processar tarefa: {e}")
            return None
    
    def run_scenario_1(self):
        """
        Cenário 1: Um único cliente envia várias tarefas para um servidor
        """
        print("\n" + "🎯" * 30)
        print("INICIANDO CENÁRIO 1")
        print("Um único cliente envia várias tarefas para um servidor")
        print("🎯" * 30 + "\n")
        
        # Lista de tarefas a serem executadas
        tasks = [
            {
                'description': 'Calcular fatorial de 5',
                'function': lambda w: w.calculate_factorial(5)
            },
            {
                'description': 'Calcular fatorial de 10',
                'function': lambda w: w.calculate_factorial(10)
            },
            {
                'description': 'Calcular fatorial de 15',
                'function': lambda w: w.calculate_factorial(15)
            },
            {
                'description': 'Ordenar lista de 20 números',
                'function': lambda w: w.sort_list([random.randint(1, 100) for _ in range(20)])
            },
            {
                'description': 'Calcular soma de 50 números',
                'function': lambda w: w.calculate_sum([random.randint(1, 100) for _ in range(50)])
            },
            {
                'description': 'Calcular fatorial de 20',
                'function': lambda w: w.calculate_factorial(20)
            },
            {
                'description': 'Ordenar lista de 30 números',
                'function': lambda w: w.sort_list([random.randint(1, 100) for _ in range(30)])
            }
        ]
        
        results = []
        
        print(f"Total de tarefas a serem enviadas: {len(tasks)}\n")
        time.sleep(1)
        
        # Envia cada tarefa
        for i, task in enumerate(tasks, 1):
            print(f"\n{'═' * 60}")
            print(f"TAREFA {i} de {len(tasks)}")
            print(f"{'═' * 60}")
            
            result = self.send_task(task['function'], task['description'])
            
            if result:
                results.append(result)
            
            # Pequena pausa entre tarefas
            time.sleep(0.5)
        
        # Exibe resumo final
        self.show_summary(results, len(tasks))
    
    def show_summary(self, results, total_tasks):
        """Exibe um resumo dos resultados"""
        print("\n\n" + "=" * 60)
        print("RESUMO DA EXECUÇÃO - CENÁRIO 1")
        print("=" * 60)
        
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   Total de tarefas enviadas: {total_tasks}")
        print(f"   Total de tarefas concluídas: {len(results)}")
        print(f"   Taxa de sucesso: {len(results)/total_tasks*100:.1f}%")
        
        if results:
            print(f"\n📋 DETALHAMENTO DAS TAREFAS:")
            print(f"   {'#':<5} {'Worker':<15} {'Tarefa':<30} {'Timestamp':<20}")
            print(f"   {'-'*5} {'-'*15} {'-'*30} {'-'*20}")
            
            for i, result in enumerate(results, 1):
                task_name = result['task']
                worker = result['worker']
                timestamp = result['timestamp']
                print(f"   {i:<5} {worker:<15} {task_name:<30} {timestamp:<20}")
        
        print("\n" + "=" * 60)
        print("✓ CENÁRIO 1 CONCLUÍDO COM SUCESSO")
        print("=" * 60 + "\n")

def main():
    """Função principal"""
    try:
        # Cria o cliente
        client = TaskClient()
        
        # Executa o cenário 1
        client.run_scenario_1()
        
    except KeyboardInterrupt:
        print("\n\n👋 Cliente encerrado pelo usuário")
    except Exception as e:
        print(f"\n✗ Erro: {e}")

if __name__ == "__main__":
    main()