#!/bin/bash

echo "--- Iniciando processo de deploy da API de classificação ---"

# Ir para o diretório raiz do projeto
cd "$(dirname "$0")/.."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Por favor, instale o Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Por favor, instale o Docker Compose."
    exit 1
fi

# Construir e iniciar o container
echo "🔄 Construindo e iniciando o container..."
cd docker
docker-compose down
docker-compose up -d --build
cd ..

# Aguardar container inicializar
echo "⏳ Aguardando container inicializar (60s)..."
sleep 60

# Testar se o container está funcionando
echo "🔍 Testando o container..."
curl -s http://localhost:7100/api/v1/status

if [ $? -eq 0 ]; then
    echo "✅ API está online!"
    
    # Testar classificação
    echo "🔍 Testando classificação..."
    TEST_RESULT=$(curl -s -X POST http://localhost:7100/api/v1/classificar \
        -H "Content-Type: application/json" \
        -d '{"texto": "Sistema não está respondendo após atualização"}')
    
    echo "Resultado do teste:"
    echo $TEST_RESULT
    
    echo "✅ Deploy concluído com sucesso!"
    echo "📊 API disponível em: http://localhost:7100"
else
    echo "❌ Falha no deploy. Verificando logs:"
    cd docker
    docker-compose logs
    cd ..
    echo "❌ Deploy falhou!"
fi 