#!/usr/bin/env python
import requests
import sys
import time
import os

# Obter a porta da variável de ambiente ou usar 7100 como padrão
PORT = os.environ.get('PORT', '7100')
API_URL = f"http://localhost:{PORT}"

def check_health():
    """Verifica se a API está funcionando corretamente"""
    url = f"{API_URL}/api/v1/status"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("✅ API está online!")
            status_data = response.json()
            print(f"Status: {status_data.get('status')}")
            print(f"Modelo: {status_data.get('modelo')}")
            print(f"Categorias: {', '.join(status_data.get('categorias', []))}")
            return 0
        else:
            print(f"❌ API retornou status code: {response.status_code}")
            return 1
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar à API: {e}")
        return 1

def test_classification():
    """Testa a classificação de um ticket"""
    url = f"{API_URL}/api/v1/classificar"
    data = {"texto": "Sistema não está respondendo após atualização"}
    
    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print("✅ Teste de classificação bem-sucedido!")
            print(f"Ticket: {result.get('ticket')}")
            print(f"Prioridade: {result.get('prioridade')}")
            print("Probabilidades:")
            for categoria, prob in result.get('probabilidades', {}).items():
                print(f"  - {categoria}: {prob*100:.1f}%")
            return 0
        else:
            print(f"❌ Teste de classificação falhou com status code: {response.status_code}")
            return 1
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao testar classificação: {e}")
        return 1

if __name__ == "__main__":
    print("Verificando saúde da API de Classificação...")
    
    # Aguarda um tempo para a API inicializar
    retries = 3
    for i in range(retries):
        health_status = check_health()
        if health_status == 0:
            break
        else:
            if i < retries - 1:
                wait_time = (i + 1) * 5
                print(f"Aguardando {wait_time} segundos antes de tentar novamente...")
                time.sleep(wait_time)
    
    # Se a API está online, testa a classificação
    if health_status == 0:
        classification_status = test_classification()
        sys.exit(classification_status)
    else:
        sys.exit(health_status) 