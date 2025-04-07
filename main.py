#!/usr/bin/env python
"""
Arquivo principal para iniciar o sistema de classificação de tickets.
Este script serve como ponto de entrada central para toda a aplicação.
"""
import os
import sys
import importlib.util
import subprocess
from pathlib import Path

# Adicionar diretórios ao PATH
PROJECT_ROOT = Path(__file__).parent.absolute()
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_DIR))

def import_module_from_file(module_name, file_path):
    """Importa um módulo Python a partir de um arquivo"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def start_app():
    """Inicia a aplicação web"""
    app_module = import_module_from_file("app_classificador", SRC_DIR / "interface" / "app_classificador.py")
    app_module.app.run(host='0.0.0.0', port=5000, debug=True)

def start_api():
    """Inicia a API REST"""
    api_module = import_module_from_file("api", SRC_DIR / "api" / "api.py")
    api_module.app.run(host='0.0.0.0', port=5000, debug=True)
    
def start_docker_api():
    """Inicia a API Docker"""
    api_module = import_module_from_file("api_docker", SRC_DIR / "api" / "api_docker.py")
    # O próprio módulo já inicia a API

def train_model():
    """Treina o modelo de classificação"""
    model_module = import_module_from_file("treinar_modelo", SRC_DIR / "model" / "treinar_modelo.py")
    # O próprio módulo já treina o modelo

def generate_data():
    """Gera dados sintéticos para treinamento"""
    data_module = import_module_from_file("gerador_dados_sinteticos", SRC_DIR / "model" / "gerador_dados_sinteticos.py")
    # O próprio módulo já gera os dados

def start_client():
    """Inicia o cliente de console"""
    client_module = import_module_from_file("cliente_api", SRC_DIR / "interface" / "cliente_api.py")
    # O próprio módulo já inicia o cliente

def show_help():
    """Mostra a ajuda do sistema"""
    print("""
Sistema de Classificação de Tickets - Menu de Ajuda

Uso: python main.py [opção]

Opções:
  app         Inicia a aplicação web
  api         Inicia a API REST
  docker-api  Inicia a API Docker na porta 7100
  train       Treina o modelo
  generate    Gera dados sintéticos
  client      Inicia o cliente console
  
  help        Mostra esta ajuda
""")

def main():
    """Função principal do programa"""
    if len(sys.argv) < 2:
        print("Por favor, especifique uma opção. Use 'python main.py help' para ver as opções disponíveis.")
        return

    option = sys.argv[1].lower()
    
    if option == "app":
        start_app()
    elif option == "api":
        start_api()
    elif option == "docker-api":
        start_docker_api()
    elif option == "train":
        train_model()
    elif option == "generate":
        generate_data()
    elif option == "client":
        start_client()
    elif option == "help":
        show_help()
    else:
        print(f"Opção '{option}' desconhecida. Use 'python main.py help' para ver as opções disponíveis.")

if __name__ == "__main__":
    main() 