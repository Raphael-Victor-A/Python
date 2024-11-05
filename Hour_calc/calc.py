def somar_horas():
    total_horas = 0
    total_minutos = 0
    
    while True:
        entrada = input("Digite o número de horas e minutos no formato 'hh:mm' ou 'sair' para finalizar: ")
        
        if entrada.lower() == 'sair':
            break
        
        try:
            horas, minutos = map(int, entrada.split(":"))
            total_horas += horas
            total_minutos += minutos
        except ValueError:
            print("Formato inválido! Use o formato 'hh:mm'.")
            continue
        
        # Converte minutos em horas se necessário
        if total_minutos >= 60:
            total_horas += total_minutos // 60
            total_minutos = total_minutos % 60
    
    print(f"Total de horas: {total_horas} horas e {total_minutos} minutos.")

somar_horas()
