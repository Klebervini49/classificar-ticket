import pickle
import pandas as pd
import sys
from pathlib import Path

print("Teste de classificação: componentes críticos com problemas estéticos")
print("=" * 70)

# Carregar modelo
with open('src/model/modelo_classificacao.pkl', 'rb') as f:
    model, vectorizer = pickle.load(f)

# Casos de teste específicos
casos_teste = [
    # Casos de componentes críticos com problemas estéticos (devem ser classificados como baixa prioridade)
    "A tela de login é feia",
    "A interface de login tem aparência antiquada",
    "O botão de pagamento está com cor errada",
    "A página de checkout tem layout desalinhado",
    "O sistema de autenticação tem design ultrapassado",
    "O módulo financeiro tem aparência desagradável",
    "A tela de login precisa ser modernizada",
    "O formulário de pagamento tem cores que não combinam",
    "Os botões de login estão com tamanho desproporcional",
    "A página inicial tem aparência amadora",
    
    # Casos de componentes críticos com problemas funcionais (devem ser alta prioridade)
    "A tela de login não está funcionando",
    "O sistema de pagamento está fora do ar",
    "O botão de login não responde aos cliques",
    "O módulo financeiro apresenta erro ao processar transações",
    "O sistema de autenticação falha ao validar credenciais",
    
    # Casos ambíguos ou de fronteira
    "A tela de login está com problemas",
    "O botão de pagamento não funciona corretamente",
    "O sistema de autenticação tem problemas de usabilidade"
]

# Testar cada caso
print("{:<35} {:<10} {:<20}".format("TEXTO", "RESULTADO", "PROBABILIDADES"))
print("-" * 70)

for texto in casos_teste:
    texto_vec = vectorizer.transform([texto])
    prioridade = model.predict(texto_vec)[0]
    probabilidades = model.predict_proba(texto_vec)[0]
    
    # Formatar probabilidades para melhor visualização
    probs = {classe: float(prob) for classe, prob in zip(model.classes_, probabilidades)}
    sorted_probs = dict(sorted(probs.items(), key=lambda item: item[1], reverse=True))
    
    # Verificar se o resultado é o esperado
    esperado = ""
    if "não" in texto.lower() or "falha" in texto.lower() or "erro" in texto.lower() or "fora do ar" in texto.lower():
        esperado = "alto"
    elif any(palavra in texto.lower() for palavra in ["feia", "feio", "aparência", "layout", "design", "cor", "cores", "visual", "modernizada"]):
        esperado = "baixo"
    
    resultado = "✓" if not esperado or prioridade == esperado else "✗"
    
    # Truncar texto para ajustar na saída
    texto_truncado = texto[:32] + "..." if len(texto) > 35 else texto
    
    # Formatar principais probabilidades
    top_prob = next(iter(sorted_probs.items()))
    prob_str = f"{top_prob[0]}: {top_prob[1]*100:.1f}%"
    
    print("{:<35} {:<10} {:<20}".format(
        texto_truncado, 
        f"{prioridade.upper()} {resultado}", 
        prob_str
    ))

# Testar especificamente o caso original que falhou
print("\nCaso específico que falhou anteriormente:")
print("-" * 70)

texto = "A tela de login é feia"
texto_vec = vectorizer.transform([texto])
prioridade = model.predict(texto_vec)[0]
probabilidades = model.predict_proba(texto_vec)[0]

# Criar um dicionário de probabilidades
probs = {classe: float(prob) for classe, prob in zip(model.classes_, probabilidades)}
print(f"Texto: \"{texto}\"")
print(f"Classificação: {prioridade.upper()}")
print("Probabilidades:")
for classe, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
    print(f"  {classe}: {prob*100:.2f}%") 