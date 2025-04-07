import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from pathlib import Path

def carregar_modelo():
    """Carrega o modelo treinado"""
    with open('src/model/modelo_classificacao.pkl', 'rb') as f:
        modelo, vectorizer = pickle.load(f)
    return modelo, vectorizer

def classificar_texto(texto, modelo, vectorizer):
    """Classifica um texto e retorna a prioridade e as probabilidades"""
    texto_vec = vectorizer.transform([texto])
    prioridade = modelo.predict(texto_vec)[0]
    probabilidades = modelo.predict_proba(texto_vec)[0]
    probs = {classe: float(prob) for classe, prob in zip(modelo.classes_, probabilidades)}
    return prioridade, probs

def avaliar_casos_teste(casos_teste, modelo, vectorizer):
    """Avalia casos de teste definidos com rótulos esperados"""
    resultados = []
    
    for caso in casos_teste:
        texto = caso['texto']
        esperado = caso['esperado']
        
        prioridade, probs = classificar_texto(texto, modelo, vectorizer)
        acerto = prioridade == esperado
        
        resultados.append({
            'texto': texto,
            'esperado': esperado,
            'predito': prioridade,
            'acerto': acerto,
            'probabilidades': probs
        })
    
    return resultados

def mostrar_matriz_confusao(resultados):
    """Exibe a matriz de confusão dos resultados"""
    y_true = [r['esperado'] for r in resultados]
    y_pred = [r['predito'] for r in resultados]
    
    labels = ['alto', 'medio', 'baixo']
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    print("\nMatriz de Confusão:")
    print("           | Predito como:")
    print("           | Alto  | Médio | Baixo")
    print("-----------+-------+-------+-------")
    for i, label in enumerate(labels):
        print(f"Real: {label.ljust(5)} | {cm[i][0]:5d} | {cm[i][1]:5d} | {cm[i][2]:5d}")
    
    # Calcular acurácia
    acertos = sum(r['acerto'] for r in resultados)
    print(f"\nAcurácia: {acertos / len(resultados):.2%}")

def mostrar_relatorio_detalhado(resultados):
    """Mostra um relatório detalhado dos casos de teste"""
    y_true = [r['esperado'] for r in resultados]
    y_pred = [r['predito'] for r in resultados]
    
    print("\nRelatório de Classificação:")
    print(classification_report(y_true, y_pred))
    
    # Mostrar casos errados
    erros = [r for r in resultados if not r['acerto']]
    if erros:
        print("\nCasos classificados incorretamente:")
        print("-" * 80)
        for erro in erros:
            print(f"Texto: {erro['texto']}")
            print(f"Esperado: {erro['esperado']}, Predito: {erro['predito']}")
            probs_sorted = sorted(erro['probabilidades'].items(), key=lambda x: x[1], reverse=True)
            print(f"Probabilidades: {' | '.join([f'{k}: {v:.2%}' for k, v in probs_sorted])}")
            print("-" * 80)

def main():
    print("Avaliação de Robustez do Modelo de Classificação")
    print("=" * 70)
    
    # Carregar modelo
    modelo, vectorizer = carregar_modelo()
    
    # Definir casos de teste com rótulos esperados
    casos_teste = [
        # Problemas estéticos em componentes críticos (baixa prioridade)
        {"texto": "A tela de login é feia", "esperado": "baixo"},
        {"texto": "A interface de login tem aparência antiquada", "esperado": "baixo"},
        {"texto": "O botão de pagamento está com cor errada", "esperado": "baixo"},
        {"texto": "A página de checkout tem layout desalinhado", "esperado": "baixo"},
        {"texto": "O sistema de autenticação tem design ultrapassado", "esperado": "baixo"},
        {"texto": "O módulo financeiro tem aparência desagradável", "esperado": "baixo"},
        {"texto": "A tela de login precisa ser modernizada", "esperado": "baixo"},
        {"texto": "O formulário de pagamento tem cores que não combinam", "esperado": "baixo"},
        {"texto": "Os botões de login estão com tamanho desproporcional", "esperado": "baixo"},
        {"texto": "A página inicial tem aparência amadora", "esperado": "baixo"},
        
        # Problemas funcionais em componentes críticos (alta prioridade)
        {"texto": "A tela de login não está funcionando", "esperado": "alto"},
        {"texto": "O sistema de pagamento está fora do ar", "esperado": "alto"},
        {"texto": "O botão de login não responde aos cliques", "esperado": "alto"},
        {"texto": "O módulo financeiro apresenta erro ao processar transações", "esperado": "alto"},
        {"texto": "O sistema de autenticação falha ao validar credenciais", "esperado": "alto"},
        {"texto": "O botão de pagamento não funciona corretamente", "esperado": "alto"},
        {"texto": "O checkout falha ao finalizar a compra", "esperado": "alto"},
        {"texto": "Não consigo fazer login no sistema", "esperado": "alto"},
        {"texto": "O gateway de pagamento retorna erro", "esperado": "alto"},
        {"texto": "A autenticação de usuários não está funcionando", "esperado": "alto"},
        
        # Casos ambíguos (casos de fronteira)
        {"texto": "A tela de login está com problemas", "esperado": "baixo"},
        {"texto": "O sistema de autenticação tem problemas de usabilidade", "esperado": "baixo"},
        {"texto": "O formulário de login está lento", "esperado": "medio"},
        {"texto": "O sistema de pagamento processa com atraso", "esperado": "medio"},
        {"texto": "Alguns usuários relatam problemas no checkout", "esperado": "medio"},
        {"texto": "O login falha ocasionalmente", "esperado": "medio"},
        {"texto": "Apenas alguns clientes não conseguem efetuar pagamento", "esperado": "medio"},
        {"texto": "A página de login tem layout confuso", "esperado": "baixo"},
        {"texto": "A estética do sistema de pagamento precisa ser melhorada", "esperado": "baixo"},
        {"texto": "Interface confusa no módulo de login", "esperado": "baixo"},
        
        # Casos com variantes de linguagem
        {"texto": "Login feio demais", "esperado": "baixo"},
        {"texto": "Sistema de pagamento com aparência horrível", "esperado": "baixo"},
        {"texto": "Checkout não funciona de jeito nenhum", "esperado": "alto"},
        {"texto": "Login quebrado completamente", "esperado": "alto"},
        {"texto": "UI do login é terrível, mas funciona", "esperado": "baixo"},
        {"texto": "Página de pagamento esteticamente desagradável", "esperado": "baixo"},
        {"texto": "Sistema lento para fazer login, mas funciona", "esperado": "medio"},
        {"texto": "Checkout por vezes apresenta travamentos", "esperado": "medio"},
        {"texto": "Aparência do login não é profissional", "esperado": "baixo"},
        {"texto": "Sistema inoperante na parte de pagamentos", "esperado": "alto"},
    ]
    
    # Avaliar casos de teste
    resultados = avaliar_casos_teste(casos_teste, modelo, vectorizer)
    
    # Exibir resultados formatados
    print(f"\nResultados dos {len(resultados)} casos de teste:")
    print("-" * 70)
    print("{:<40} {:<10} {:<15} {:<15}".format("TEXTO", "ESPERADO", "PREDITO", "PROBABILIDADE"))
    print("-" * 70)
    
    for resultado in resultados:
        texto = resultado['texto'][:37] + "..." if len(resultado['texto']) > 40 else resultado['texto']
        esperado = resultado['esperado'].upper()
        predito = resultado['predito'].upper()
        acerto = "✓" if resultado['acerto'] else "✗"
        
        # Encontrar a probabilidade da classe predita
        prob = resultado['probabilidades'][resultado['predito']] * 100
        
        print("{:<40} {:<10} {:<15} {:<15}".format(
            texto, 
            esperado, 
            f"{predito} {acerto}", 
            f"{prob:.1f}%"
        ))
    
    # Mostrar matriz de confusão
    mostrar_matriz_confusao(resultados)
    
    # Mostrar relatório detalhado
    mostrar_relatorio_detalhado(resultados)

if __name__ == "__main__":
    main() 