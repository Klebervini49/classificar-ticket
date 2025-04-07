import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os
from pathlib import Path

# Obter o diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = Path(__file__).parent.absolute()

# Garantir que os diretórios existem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def treinar_modelo():
    # Carregar o dataset
    print("Carregando dataset...")
    dataset_path = DATA_DIR / "dataset_tickets_prioridade.csv"
    
    if not os.path.exists(dataset_path):
        print(f"Dataset não encontrado em {dataset_path}. Gerando dados sintéticos...")
        from . import gerador_dados_sinteticos
        dataset_path = gerador_dados_sinteticos.main()
    
    df = pd.read_csv(dataset_path, encoding='utf-8')

    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        df['texto'], df['prioridade'], test_size=0.3, random_state=42
    )

    # Vetorizar texto
    print("Preparando textos...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Treinar modelo
    print("Treinando modelo...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_vec, y_train)

    # Avaliar modelo
    print("Avaliando modelo...")
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Acurácia: {accuracy:.4f}")
    print("\nRelatório de classificação:")
    print(report)

    # Salvar modelo e vectorizer
    print("Salvando modelo...")
    modelo_path = MODEL_DIR / "modelo_classificacao.pkl"
    with open(modelo_path, 'wb') as f:
        pickle.dump((model, vectorizer), f)

    print(f"Modelo salvo como '{modelo_path}'")
    
    return model, vectorizer

def testar_exemplos(model, vectorizer):
    # Exemplo de uso
    print("\nExemplo de classificação:")
    exemplos = [
        "Sistema não está respondendo após atualização",
        "Botão de login está com cor errada",
        "Usuários relatam lentidão ao gerar relatórios",
        "O sistema é feio",
        "O sistema é ruim",
        "Sistema deu erro"
    ]

    # Vetorizar exemplos
    exemplos_vec = vectorizer.transform(exemplos)
    predicoes = model.predict(exemplos_vec)
    probabilidades = model.predict_proba(exemplos_vec)

    for i, exemplo in enumerate(exemplos):
        print(f"\nTexto: {exemplo}")
        print(f"Classificação: {predicoes[i]}")
        probs = {classe: float(prob) for classe, prob in zip(model.classes_, probabilidades[i])}
        print(f"Probabilidades: {probs}")
        
def main():
    model, vectorizer = treinar_modelo()
    testar_exemplos(model, vectorizer)
    return model, vectorizer

if __name__ == "__main__":
    main() 