#!/bin/bash

echo "--- Iniciando processo de construção e execução do container Docker ---"

# Ir para o diretório raiz do projeto
cd "$(dirname "$0")/.."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Por favor, instale o Docker."
    exit 1
fi

# Parar e remover o container existente
echo "🔄 Parando containers existentes..."
cd docker
docker compose down || docker-compose down
cd ..

# Gerar dados e treinar modelo para garantir que está disponível
echo "🔄 Gerando dados e treinando modelo..."
python -m src.model.gerador_dados_sinteticos
python -m src.model.treinar_modelo

# Verificar se o modelo foi gerado
if [ -f "src/model/modelo_classificacao.pkl" ]; then
    echo "✅ Modelo gerado com sucesso!"
    # Copiar modelo para diretório raiz para garantir que todos os caminhos funcionam
    cp src/model/modelo_classificacao.pkl ./modelo_classificacao.pkl
    echo "✅ Modelo copiado para a raiz do projeto."
else
    echo "❌ Falha ao gerar modelo. Verifique os erros acima."
    exit 1
fi

# Remover imagem existente para forçar reconstrução
echo "🔄 Removendo imagem antiga para reconstrução..."
docker rmi -f api-classificacao || true

# Construir e iniciar o container
echo "🔄 Construindo e iniciando o container..."
cd docker
docker compose up -d --build || docker-compose up -d --build
cd ..


# Testar se a API está funcionando
echo "🔍 Testando a API..."
curl -s http://localhost:7100/api/v1/status

if [ $? -eq 0 ]; then
    echo "✅ API está online em http://localhost:7100"
    
    # Testar classificação
    echo "🔍 Testando classificação..."
    TEST_RESULT=$(curl -s -X POST http://localhost:7100/api/v1/classificar \
        -H "Content-Type: application/json" \
        -d '{"texto": "Sistema não está respondendo após atualização"}')
    
    echo "Resultado do teste:"
    echo $TEST_RESULT
    
    echo "✅ API está funcionando corretamente!"
else
    echo "❌ Falha na API. Verificando logs:"
    cd docker
    docker compose logs || docker-compose logs
    cd ..
fi

# Testar se a interface web está funcionando
echo "🔍 Testando a interface web..."
curl -s http://localhost:5000

if [ $? -eq 0 ]; then
    echo "✅ Interface web está online em http://localhost:5000"
else
    echo "❌ Falha na interface web. Verificando logs:"
    cd docker
    docker compose logs || docker-compose logs
    cd ..
fi

echo "📊 Container Docker rodando com:"
echo "- API: http://localhost:7100"
echo "- Interface Web: http://localhost:5000"
echo ""
echo "Para parar o container, execute:"
echo "cd docker && docker compose down" 