import pickle
import sys
from pathlib import Path

# Carregar modelo
with open('src/model/modelo_classificacao.pkl', 'rb') as f:
    model, vectorizer = pickle.load(f)

# Testar frases específicas
frases = [
    # Frases simples de "não funciona"
    'A tela x não está funcionando',
    'A tela x não funciona',
    
    # Com contexto de funcionalidade específica
    'A tela de login não está funcionando',
    'A tela de relatórios não está funcionando',
    'A tela de ajuda não está funcionando',
    
    # Com contexto de severidade/impacto
    'A tela x não está funcionando para todos os usuários',
    'A tela x não está funcionando para alguns usuários',
    'A tela x não está funcionando apenas visualmente',
    'A tela x não está funcionando completamente',
    'A tela x não está funcionando intermitentemente',
    
    # Variações com contexto
    'A tela de pagamento não está funcionando para todos os usuários',
    'A tela de pagamento não está funcionando intermitentemente',
    'A tela de preferências não está funcionando completamente',
    
    # Frases com diferentes verbos
    'O sistema de login está com problema',
    'O módulo de relatórios parou de funcionar',
    'A função de backup está inoperante',
    
    # Frases com contexto implícito de severidade
    'Sistema completamente fora do ar',
    'Tela principal não funciona, empresa paralisada',
    'Pequeno erro visual na tela de ajuda',
    'Algumas funcionalidades apresentando erros intermitentes'
]

print("Resultados da classificação:")
print("=" * 80)

for frase in frases:
    frase_vec = vectorizer.transform([frase])
    prioridade = model.predict(frase_vec)[0]
    probabilidades = model.predict_proba(frase_vec)[0]
    
    # Ordenar probabilidades para melhor visualização
    probs = {classe: float(prob) for classe, prob in zip(model.classes_, probabilidades)}
    sorted_probs = dict(sorted(probs.items(), key=lambda item: item[1], reverse=True))
    
    # Formatar a saída
    probs_formatted = " | ".join([f"{k}: {v*100:.1f}%" for k, v in sorted_probs.items()])
    
    print(f'\nTexto: "{frase}"')
    print(f'Classificação: {prioridade.upper()}')
    print(f'Probabilidades: {probs_formatted}') 