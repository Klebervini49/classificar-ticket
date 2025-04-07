# Sistema de Classificação de Tickets por Prioridade

Um sistema inteligente que classifica tickets em prioridades (alto, médio, baixo) utilizando aprendizado de máquina.

## 🚀 Início Rápido

Para iniciar o sistema rapidamente usando Docker:

```bash
# Tornar o script executável (apenas uma vez)
chmod +x scripts/iniciar_docker.sh

# Executar o sistema
./scripts/iniciar_docker.sh
```

Após executar o script, o sistema estará disponível em:
- **API REST**: http://localhost:7100
- **Interface Web**: http://localhost:5000

## 📋 Funcionalidades

- ✅ Classificação automática de tickets por prioridade
- ✅ Interface web amigável para testar a classificação
- ✅ API REST para integração com outros sistemas
- ✅ Geração de dados sintéticos e treinamento automático
- ✅ Containerização com Docker para implantação fácil

## 🛠️ Requisitos

- Python 3.6+
- Docker (para uso com container)
- Bibliotecas Python (pandas, numpy, scikit-learn, flask, flask-cors, requests)

## 📦 Estrutura do Projeto

```
classificacao/
├── data/               # Dados e modelos gerados
├── docker/             # Configurações Docker
├── scripts/            # Scripts úteis (incluindo iniciar_docker.sh)
├── src/                # Código fonte
│   ├── api/            # API REST 
│   ├── interface/      # Interfaces de usuário
│   ├── model/          # Modelos e algoritmos
│   └── utils/          # Utilitários
├── main.py             # Ponto de entrada principal
└── requirements.txt    # Dependências do projeto
```

## 🐳 Docker (Recomendado)

A maneira mais fácil de executar este projeto é usando Docker com o script de inicialização:

```bash
./scripts/iniciar_docker.sh
```

Este script automatiza todo o processo:
1. Verifica se o Docker está instalado
2. Gera dados sintéticos e treina o modelo
3. Constrói e inicia o container
4. Testa a API e interface web
5. Exibe as URLs de acesso

### Testando o Sistema

Após iniciar o Docker, você pode:

- Acessar a interface web em **http://localhost:5000**
- Testar a API diretamente:
  ```bash
  curl -X POST http://localhost:7100/api/v1/classificar \
      -H "Content-Type: application/json" \
      -d '{"texto": "Sistema não está respondendo após atualização"}'
  ```

### Gerenciando o Container

```bash
# Ver logs
cd docker && docker compose logs

# Reiniciar o container
cd docker && docker compose restart

# Parar o container
cd docker && docker compose down
```

## 🖥️ Execução Local (Sem Docker)

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Comandos Disponíveis

```bash
# Gerar dados sintéticos
python main.py generate

# Treinar o modelo
python main.py train

# Iniciar a aplicação web
python main.py app

# Iniciar a API REST
python main.py api

# Iniciar a API na porta 7100
python main.py docker-api

# Iniciar o cliente console
python main.py client
```

## 🔍 Exemplos de Uso da API

### Classificação de um Ticket

```python
import requests

url = "http://localhost:7100/api/v1/classificar"
dados = {"texto": "Sistema não está respondendo após atualização"}

resposta = requests.post(url, json=dados)
resultado = resposta.json()

print(f"Prioridade: {resultado['prioridade']}")
```

### Classificação em Lote

```python
import requests

url = "http://localhost:7100/api/v1/classificar-lote"
dados = {
    "tickets": [
        "Sistema não está respondendo após atualização",
        "Botão de login está com cor errada"
    ]
}

resposta = requests.post(url, json=dados)
resultado = resposta.json()

for r in resultado["resultados"]:
    print(f"Ticket: {r['ticket']}")
    print(f"Prioridade: {r['prioridade']}")
```

## 🔧 Solução de Problemas

Se encontrar problemas ao executar o sistema:

1. **Erro de permissão no script**: Execute `chmod +x scripts/iniciar_docker.sh`

2. **Portas já em uso**: Verifique se as portas 7100 e 5000 estão livres

3. **Modelo não encontrado**: O script deve gerar automaticamente. Se falhar, execute:
   ```bash
   python -m src.model.gerador_dados_sinteticos
   python -m src.model.treinar_modelo
   ```

4. **Logs do Docker**: Verifique os logs com `cd docker && docker compose logs` 
