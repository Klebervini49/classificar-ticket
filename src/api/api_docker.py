import pickle
import os
import pandas as pd
from flask import Flask, request, jsonify, render_template_string

# Configurar a porta a partir da variável de ambiente ou usar 7100 como padrão
PORT = int(os.environ.get('PORT', 7100))

# Tentar vários caminhos possíveis para o modelo
model_paths = [
    'modelo_classificacao.pkl',  # Raiz atual
    '/app/modelo_classificacao.pkl',  # Raiz do container
    os.path.join(os.path.dirname(__file__), '..', 'model', 'modelo_classificacao.pkl')  # Caminho relativo
]

print("Procurando modelo...")
for path in model_paths:
    print(f"Verificando modelo em {path}...")
    if os.path.exists(path):
        MODEL_PATH = path
        print(f"✅ Modelo encontrado em: {MODEL_PATH}")
        break
else:
    print("❌ Modelo não encontrado em nenhum caminho conhecido.")
    MODEL_PATH = 'modelo_classificacao.pkl'
    # Executar a geração de dados se necessário
    if not os.path.exists('dataset_tickets_prioridade.csv'):
        print("Gerando dados sintéticos...")
        import subprocess
        subprocess.run(['python', '-m', 'src.model.gerador_dados_sinteticos'])
    
    # Treinar o modelo
    print("Treinando modelo...")
    import subprocess
    subprocess.run(['python', '-m', 'src.model.treinar_modelo'])

# Carregar modelo
print(f"Carregando modelo de classificação de {MODEL_PATH}...")
try:
    with open(MODEL_PATH, 'rb') as f:
        model, vectorizer = pickle.load(f)
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar modelo: {e}")
    raise

app = Flask(__name__)

# Template HTML para a documentação
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>API de Classificação de Prioridade de Tickets</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        pre { background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }
        h3 { margin-top: 30px; color: #333; }
    </style>
</head>
<body>
    <h1>API de Classificação de Prioridade de Tickets</h1>
    <p>Esta API permite classificar a prioridade de tickets com base em sua descrição.</p>
    
    <h2>Endpoints Disponíveis</h2>
    
    <h3>1. Classificar um Ticket</h3>
    <p><code>POST /api/v1/classificar</code></p>
    <p>Classifica um único ticket.</p>
    <p>Exemplo de requisição:</p>
    <pre>
    {
        "texto": "Sistema não está respondendo após atualização"
    }
    </pre>
    <p>Exemplo de resposta:</p>
    <pre>
    {
        "ticket": "Sistema não está respondendo após atualização",
        "prioridade": "alto",
        "probabilidades": {
            "alto": 0.75,
            "medio": 0.20,
            "baixo": 0.05
        }
    }
    </pre>
    
    <h3>2. Classificar Múltiplos Tickets</h3>
    <p><code>POST /api/v1/classificar-lote</code></p>
    <p>Classifica múltiplos tickets em uma única requisição.</p>
    <p>Exemplo de requisição:</p>
    <pre>
    {
        "tickets": [
            "Sistema não está respondendo após atualização",
            "Botão de login está com cor errada"
        ]
    }
    </pre>
    
    <h3>3. Verificar Status da API</h3>
    <p><code>GET /api/v1/status</code></p>
    <p>Retorna o status atual da API e informações sobre o modelo.</p>
    
    <h2>Exemplo em cURL</h2>
    <pre>
    curl -X POST http://localhost:7100/api/v1/classificar \\
        -H "Content-Type: application/json" \\
        -d '{"texto": "Sistema não está respondendo após atualização"}'
    </pre>
    
    <h2>Exemplo em Python</h2>
    <pre>
    import requests
    
    url = "http://localhost:7100/api/v1/classificar"
    data = {"texto": "Sistema não está respondendo após atualização"}
    
    response = requests.post(url, json=data)
    resultado = response.json()
    
    print(f"Prioridade: {resultado['prioridade']}")
    </pre>
</body>
</html>
'''

@app.route('/')
def documentacao():
    return render_template_string(HTML)

@app.route('/api/v1/classificar', methods=['POST'])
def classificar_ticket():
    """
    Endpoint para classificar a prioridade de um ticket
    Recebe um JSON com o campo 'texto' contendo a descrição do ticket
    Retorna a classificação de prioridade e as probabilidades de cada categoria
    """
    if not request.json or 'texto' not in request.json:
        return jsonify({
            'erro': 'Texto do ticket não fornecido. Envie um JSON com o campo "texto".'
        }), 400
    
    texto = request.json['texto']
    
    # Classificar o texto
    texto_vec = vectorizer.transform([texto])
    prioridade = model.predict(texto_vec)[0]
    probabilidades = model.predict_proba(texto_vec)[0]
    
    # Criar um dicionário de probabilidades
    probs = {classe: float(prob) for classe, prob in zip(model.classes_, probabilidades)}
    
    return jsonify({
        'ticket': texto,
        'prioridade': prioridade,
        'probabilidades': probs
    })

@app.route('/api/v1/classificar-lote', methods=['POST'])
def classificar_lote():
    """
    Endpoint para classificar múltiplos tickets em lote
    Recebe um JSON com o campo 'tickets' contendo uma lista de descrições
    Retorna uma lista com as classificações de cada ticket
    """
    if not request.json or 'tickets' not in request.json:
        return jsonify({
            'erro': 'Lista de tickets não fornecida. Envie um JSON com o campo "tickets".'
        }), 400
    
    tickets = request.json['tickets']
    if not isinstance(tickets, list):
        return jsonify({
            'erro': 'O campo "tickets" deve ser uma lista de strings.'
        }), 400
    
    # Classificar todos os tickets
    textos_vec = vectorizer.transform(tickets)
    prioridades = model.predict(textos_vec)
    todas_probabilidades = model.predict_proba(textos_vec)
    
    resultados = []
    for i, ticket in enumerate(tickets):
        # Criar um dicionário de probabilidades para este ticket
        probs = {classe: float(prob) for classe, prob in zip(model.classes_, todas_probabilidades[i])}
        
        resultados.append({
            'ticket': ticket,
            'prioridade': prioridades[i],
            'probabilidades': probs
        })
    
    return jsonify({
        'total': len(resultados),
        'resultados': resultados
    })

@app.route('/api/v1/status', methods=['GET'])
def status():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'online',
        'modelo': 'Classificador de prioridade de tickets',
        'categorias': model.classes_.tolist(),
        'porta': PORT
    })

if __name__ == '__main__':
    print(f"Iniciando API de classificação de tickets na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False) 