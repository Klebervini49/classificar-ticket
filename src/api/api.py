import pickle
import pandas as pd
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Carregar modelo
print("Carregando modelo de classificação...")

# Tentar vários caminhos possíveis para o modelo
model_paths = [
    'modelo_classificacao.pkl',  # Raiz atual
    '/app/modelo_classificacao.pkl',  # Raiz do container
    os.path.join(os.path.dirname(__file__), '..', 'model', 'modelo_classificacao.pkl')  # Caminho relativo
]

model = None
vectorizer = None

for path in model_paths:
    try:
        print(f"Tentando carregar modelo de: {path}")
        with open(path, 'rb') as f:
            model, vectorizer = pickle.load(f)
        print(f"✅ Modelo carregado com sucesso de: {path}")
        break
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {path}")
        continue

if model is None:
    raise FileNotFoundError("Não foi possível encontrar o arquivo do modelo em nenhum caminho!")

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

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
        'categorias': model.classes_.tolist()
    })

# Documentação da API na página inicial
@app.route('/', methods=['GET'])
def documentacao():
    return """
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
            curl -X POST http://localhost:5000/api/v1/classificar \\
                -H "Content-Type: application/json" \\
                -d '{"texto": "Sistema não está respondendo após atualização"}'
            </pre>
            
            <h2>Exemplo em Python</h2>
            <pre>
            import requests
            
            url = "http://localhost:5000/api/v1/classificar"
            data = {"texto": "Sistema não está respondendo após atualização"}
            
            response = requests.post(url, json=data)
            resultado = response.json()
            
            print(f"Prioridade: {resultado['prioridade']}")
            print(f"Probabilidades: {resultado['probabilidades']}")
            </pre>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("Iniciando API de classificação de tickets...")
    app.run(host='0.0.0.0', port=5000, debug=True) 