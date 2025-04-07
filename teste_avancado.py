import pickle
import pandas as pd

def main():
    print("Teste Avançado de Casos Específicos")
    print("=" * 70)
    
    # Carregar modelo
    with open('src/model/modelo_classificacao.pkl', 'rb') as f:
        modelo, vectorizer = pickle.load(f)
    
    # Casos específicos para testar
    casos_teste = [
        # Combinações de estética e funcionalidade (verificar se problema funcional tem mais peso)
        "A tela de login é feia e não funciona direito",
        "O sistema de pagamento tem aparência ruim e falha às vezes",
        "Login com design terrível que trava ocasionalmente",
        
        # Casos ambíguos
        "A página de checkout tem problemas de usabilidade e aparência",
        "A interface de pagamento é confusa mas os pagamentos são processados",
        
        # Descrições incomuns
        "A UI está uma zona no login mas conseguimos usar",
        "Interface do século passado no sistema de pagamento",
        "Está impossível acessar o sistema de login",
        
        # Casos com informações contraditórias
        "O login tem problemas visuais e não é possível acessar o sistema",
        "O sistema é feio mas funcional, porém ultimamente não consigo acessar"
    ]
    
    # Testar cada caso
    print("{:<45} {:<10} {:<25}".format("TEXTO", "RESULTADO", "PROBABILIDADES"))
    print("-" * 80)
    
    for texto in casos_teste:
        texto_vec = vectorizer.transform([texto])
        prioridade = modelo.predict(texto_vec)[0]
        probabilidades = modelo.predict_proba(texto_vec)[0]
        
        # Formatar probabilidades e ordenar
        probs = {classe: float(prob) for classe, prob in zip(modelo.classes_, probabilidades)}
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        
        # Truncar texto para ajustar na saída
        texto_truncado = texto[:42] + "..." if len(texto) > 45 else texto
        
        # Formatar todas as probabilidades
        probs_fmt = " | ".join([f"{k}: {v*100:.1f}%" for k, v in sorted_probs])
        
        print("{:<45} {:<10} {:<25}".format(
            texto_truncado, 
            prioridade.upper(), 
            probs_fmt[:25] + "..." if len(probs_fmt) > 25 else probs_fmt
        ))

if __name__ == "__main__":
    main() 