#!/bin/bash

echo "Executando sistema usando Docker diretamente (sem PM2)"

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Por favor, instale o Docker."
    exit 1
fi

# Gerar dados e treinar modelo
echo "🔄 Gerando dados e treinando modelo..."
python -m src.model.gerador_dados_sinteticos
python -m src.model.treinar_modelo

# Copiar modelo para raiz
echo "🔄 Copiando modelo para raiz..."
cp src/model/modelo_classificacao.pkl ./modelo_classificacao.pkl

# Parar containers existentes
echo "🔄 Parando containers existentes..."
docker stop api-classificacao 2>/dev/null || true
docker rm api-classificacao 2>/dev/null || true

# Construir imagem
echo "🔄 Construindo imagem..."
docker build -t api-classificacao:latest .

# Iniciar container
echo "🔄 Iniciando container..."
docker run -d --name api-classificacao -p 7100:7100 -p 5000:5000 api-classificacao:latest

# Aguardar inicialização
echo "⏳ Aguardando inicialização dos serviços..."
sleep 15

# Verificar se os serviços estão rodando
echo "🔍 Verificando serviços..."

# Verificar API
if curl -s http://localhost:7100/api/v1/status > /dev/null; then
    echo "✅ API está funcionando em http://localhost:7100"
else
    echo "❌ API não está respondendo em http://localhost:7100"
    docker logs api-classificacao
fi

# Verificar interface web
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Interface web está funcionando em http://localhost:5000"
else 
    echo "❌ Interface web não está respondendo em http://localhost:5000"
    docker logs api-classificacao
fi

echo ""
echo "📊 Comandos úteis:"
echo "- Ver logs: docker logs -f api-classificacao"
echo "- Parar: docker stop api-classificacao"
echo "- Reiniciar: docker restart api-classificacao" 