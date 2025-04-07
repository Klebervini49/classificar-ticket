import requests
import json

def classificar_ticket(texto):
    """Classifica um único ticket usando a API"""
    url = "http://localhost:5000/api/v1/classificar"
    dados = {"texto": texto}
    
    try:
        resposta = requests.post(url, json=dados)
        resposta.raise_for_status()  # Levantar exceção para erros HTTP
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao classificar ticket: {e}")
        return None

def classificar_lote(tickets):
    """Classifica múltiplos tickets usando a API"""
    url = "http://localhost:5000/api/v1/classificar-lote"
    dados = {"tickets": tickets}
    
    try:
        resposta = requests.post(url, json=dados)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao classificar lote: {e}")
        return None

def verificar_status():
    """Verifica o status da API"""
    url = "http://localhost:5000/api/v1/status"
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao verificar status: {e}")
        return None

def formatar_resultado(resultado):
    """Formata o resultado para exibição"""
    if not resultado:
        return "Não foi possível obter resultado"
    
    if 'erro' in resultado:
        return f"Erro: {resultado['erro']}"
    
    if 'ticket' in resultado:  # Resultado único
        texto = resultado['ticket']
        prioridade = resultado['prioridade'].upper()
        probabilities = resultado['probabilidades']
        
        # Ordenar probabilidades do maior para o menor
        sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        
        resultado_formatado = f"Ticket: {texto}\n"
        resultado_formatado += f"Prioridade: {prioridade}\n"
        resultado_formatado += "Probabilidades:\n"
        
        for categoria, prob in sorted_probs:
            resultado_formatado += f"  - {categoria}: {prob*100:.1f}%\n"
        
        return resultado_formatado
    
    elif 'resultados' in resultado:  # Resultado em lote
        resultado_formatado = f"Total de tickets classificados: {resultado['total']}\n\n"
        
        for i, res in enumerate(resultado['resultados'], 1):
            resultado_formatado += f"--- Ticket {i} ---\n"
            resultado_formatado += f"Texto: {res['ticket']}\n"
            resultado_formatado += f"Prioridade: {res['prioridade'].upper()}\n"
            
            # Ordenar probabilidades do maior para o menor
            sorted_probs = sorted(res['probabilidades'].items(), key=lambda x: x[1], reverse=True)
            resultado_formatado += "Probabilidades:\n"
            
            for categoria, prob in sorted_probs:
                resultado_formatado += f"  - {categoria}: {prob*100:.1f}%\n"
            
            resultado_formatado += "\n"
        
        return resultado_formatado
    
    return f"Formato de resultado desconhecido: {json.dumps(resultado, indent=2)}"

def menu():
    while True:
        print("\n===== Cliente API de Classificação de Tickets =====")
        print("1. Classificar um ticket")
        print("2. Classificar múltiplos tickets")
        print("3. Verificar status da API")
        print("4. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            texto = input("Digite a descrição do ticket: ")
            if texto:
                resultado = classificar_ticket(texto)
                print("\nResultado:")
                print(formatar_resultado(resultado))
        
        elif opcao == "2":
            tickets = []
            while True:
                texto = input("Digite a descrição do ticket (ou deixe em branco para finalizar): ")
                if not texto:
                    break
                tickets.append(texto)
            
            if tickets:
                resultado = classificar_lote(tickets)
                print("\nResultado:")
                print(formatar_resultado(resultado))
            else:
                print("Nenhum ticket informado.")
        
        elif opcao == "3":
            resultado = verificar_status()
            if resultado:
                print("\nStatus da API:")
                print(f"Status: {resultado['status']}")
                print(f"Modelo: {resultado['modelo']}")
                print(f"Categorias: {', '.join(resultado['categorias'])}")
            else:
                print("Não foi possível verificar o status da API.")
        
        elif opcao == "4":
            print("Encerrando o cliente...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    print("Cliente para API de Classificação de Tickets")
    menu() 