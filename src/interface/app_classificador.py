import pickle
import pandas as pd
import os
from flask import Flask, request, jsonify, render_template_string

# Carregar modelo
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

app = Flask(__name__)

# Template HTML
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Classificador de Prioridade de Tickets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        textarea {
            width: 100%;
            height: 100px;
            margin-bottom: 10px;
            padding: 10px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .alto {
            background-color: #ffcccc;
        }
        .medio {
            background-color: #ffffcc;
        }
        .baixo {
            background-color: #ccffcc;
        }
        .probability-bar {
            height: 20px;
            margin: 5px 0;
            display: flex;
        }
        .probability-segment {
            height: 100%;
            display: inline-block;
            text-align: center;
            color: white;
        }
    </style>
</head>
<body>
    <h1>Classificador de Prioridade de Tickets</h1>
    <p>Digite a descrição do ticket para classificar sua prioridade:</p>
    
    <textarea id="ticketText" placeholder="Exemplo: Sistema não está respondendo após atualização"></textarea>
    <button onclick="classifyTicket()">Classificar</button>
    
    <div id="result" class="result" style="display: none;"></div>
    
    <script>
        function classifyTicket() {
            const ticketText = document.getElementById('ticketText').value;
            if (!ticketText) {
                alert('Por favor, digite a descrição do ticket.');
                return;
            }
            
            fetch('/classificar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ texto: ticketText }),
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('result');
                resultDiv.className = 'result ' + data.prioridade;
                
                let html = `<h2>Resultado:</h2>`;
                html += `<p><strong>Prioridade:</strong> ${data.prioridade.toUpperCase()}</p>`;
                
                // Create probability bar
                html += `<p><strong>Probabilidades:</strong></p>`;
                html += `<div class="probability-bar">`;
                
                // Colors for each priority
                const colors = {
                    'alto': '#ff6666',
                    'medio': '#ffcc66',
                    'baixo': '#66cc66'
                };
                
                // Add segments for each probability
                for (const [priority, prob] of Object.entries(data.probabilidades)) {
                    const width = Math.round(prob * 100);
                    html += `<div class="probability-segment" style="width: ${width}%; background-color: ${colors[priority]};">
                               ${priority}: ${Math.round(prob * 100)}%
                             </div>`;
                }
                
                html += `</div>`;
                
                resultDiv.innerHTML = html;
                resultDiv.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao classificar o ticket.');
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/classificar', methods=['POST'])
def classificar():
    data = request.json
    texto = data.get('texto', '')
    
    # Classificar o texto
    texto_vec = vectorizer.transform([texto])
    prioridade = model.predict(texto_vec)[0]
    probabilidades = model.predict_proba(texto_vec)[0]
    
    # Criar um dicionário de probabilidades
    probs = {classe: float(prob) for classe, prob in zip(model.classes_, probabilidades)}
    
    return jsonify({
        'prioridade': prioridade,
        'probabilidades': probs
    })

if __name__ == '__main__':
    app.run(debug=True) 