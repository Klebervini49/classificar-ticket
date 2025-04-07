import os
import sys
import subprocess
import time
import webbrowser

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import pandas
        import numpy
        import sklearn
        import flask
        import flask_cors
        import requests
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Falta instalar algumas dependências: {e}")
        return False

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("Instalando dependências via requirements.txt...")
    if os.path.exists("requirements.txt"):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
    else:
        print("⚠️ Arquivo requirements.txt não encontrado. Instalando dependências manualmente...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "pandas", "numpy", "scikit-learn", "flask", "flask-cors", "requests"
        ])

def verificar_arquivo(arquivo):
    """Verifica se um arquivo existe"""
    return os.path.isfile(arquivo)

def menu():
    """Menu principal do sistema"""
    while True:
        print("\n===== Sistema de Classificação de Tickets =====")
        print("1. Gerar dados sintéticos")
        print("2. Treinar modelo")
        print("3. Iniciar interface web")
        print("4. Iniciar API REST")
        print("5. Iniciar cliente de API")
        print("6. Iniciar tudo (API + Interface Web)")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            print("Gerando dados sintéticos...")
            subprocess.run([sys.executable, "gerador_dados_sinteticos.py"])
        
        elif opcao == "2":
            if not verificar_arquivo("dataset_tickets_prioridade.csv"):
                print("⚠️  Dataset não encontrado. Execute a opção 1 primeiro.")
                continue
                
            print("Treinando modelo...")
            subprocess.run([sys.executable, "treinar_modelo.py"])
        
        elif opcao == "3":
            if not verificar_arquivo("modelo_classificacao.pkl"):
                print("⚠️  Modelo não encontrado. Execute a opção 2 primeiro.")
                continue
                
            print("Iniciando interface web...")
            print("Acesse: http://127.0.0.1:5000")
            print("Pressione Ctrl+C para encerrar")
            
            # Abrir navegador após 2 segundos
            def abrir_navegador():
                time.sleep(2)
                webbrowser.open("http://127.0.0.1:5000")
            
            import threading
            threading.Thread(target=abrir_navegador, daemon=True).start()
            
            subprocess.run([sys.executable, "app_classificador.py"])
        
        elif opcao == "4":
            if not verificar_arquivo("modelo_classificacao.pkl"):
                print("⚠️  Modelo não encontrado. Execute a opção 2 primeiro.")
                continue
                
            print("Iniciando API REST...")
            print("API disponível em: http://localhost:5000")
            print("Pressione Ctrl+C para encerrar")
            
            # Abrir documentação da API após 2 segundos
            def abrir_navegador():
                time.sleep(2)
                webbrowser.open("http://localhost:5000")
            
            import threading
            threading.Thread(target=abrir_navegador, daemon=True).start()
            
            subprocess.run([sys.executable, "api.py"])
        
        elif opcao == "5":
            print("Iniciando cliente da API...")
            print("Certifique-se que a API esteja rodando (opção 4)")
            subprocess.run([sys.executable, "cliente_api.py"])
        
        elif opcao == "6":
            if not verificar_arquivo("modelo_classificacao.pkl"):
                print("⚠️  Modelo não encontrado. Execute a opção 2 primeiro.")
                continue
                
            print("Iniciando API REST e abrindo cliente...")
            print("API disponível em: http://localhost:5000")
            print("Pressione Ctrl+C para encerrar")
            
            # Abrir documentação da API após 2 segundos
            def abrir_navegador():
                time.sleep(2)
                webbrowser.open("http://localhost:5000")
                time.sleep(1)
                # Iniciar cliente em novo processo
                subprocess.Popen([sys.executable, "cliente_api.py"], 
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            import threading
            threading.Thread(target=abrir_navegador, daemon=True).start()
            
            subprocess.run([sys.executable, "api.py"])
        
        elif opcao == "7":
            print("Encerrando sistema...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    print("Sistema de Classificação de Prioridade de Tickets\n")
    
    if not verificar_dependencias():
        resposta = input("Deseja instalar as dependências agora? (s/n): ")
        if resposta.lower() == "s":
            instalar_dependencias()
        else:
            print("Não é possível continuar sem as dependências.")
            sys.exit(1)
    
    menu() 