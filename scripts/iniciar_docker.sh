#!/bin/bash

echo "--- Iniciando processo de construção e execução do container Docker ---"

# Ir para o diretório raiz do projeto
cd "$(dirname "$0")/.."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Por favor, instale o Docker."
    exit 1
fi

# Verificar se as portas 7100 e 5000 estão em uso
for porta in 7100 5000; do
    if command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":$porta "; then
            echo "❌ A porta $porta já está em uso. Por favor, libere esta porta antes de continuar."
            exit 1
        fi
    elif command -v lsof &> /dev/null; then
        if lsof -i ":$porta" &> /dev/null; then
            echo "❌ A porta $porta já está em uso. Por favor, libere esta porta antes de continuar."
            exit 1
        fi
    else
        echo "⚠️ Não foi possível verificar se a porta $porta está em uso. Continuando mesmo assim..."
    fi
done

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

# Aguardar inicialização - tempo aumentado
echo "⏳ Aguardando inicialização dos serviços (90s)..."
for i in {1..90}; do
    echo -n "."
    sleep 1
    # A cada 10 segundos, tentar acessar o status
    if [ $((i % 10)) -eq 0 ]; then
        if curl -s http://localhost:7100/api/v1/status > /dev/null; then
            echo "✅ API respondendo na porta 7100!"
            break
        fi
    fi
done
echo ""

# Verificar logs para diagnosticar problemas
echo "📋 Verificando logs do container:"
cd docker
docker compose logs --tail 30 || docker-compose logs --tail 30
cd ..

# Testar se a API está funcionando
echo "🔍 Testando a API..."
for retry in {1..3}; do
    API_RESPONSE=$(curl -s http://localhost:7100/api/v1/status)
    if [ -n "$API_RESPONSE" ]; then
        echo "✅ API está online em http://localhost:7100"
        echo "Resposta: $API_RESPONSE"
        
        # Testar classificação
        echo "🔍 Testando classificação..."
        TEST_RESULT=$(curl -s -X POST http://localhost:7100/api/v1/classificar \
            -H "Content-Type: application/json" \
            -d '{"texto": "Sistema não está respondendo após atualização"}')
        
        if [ -n "$TEST_RESULT" ]; then
            echo "Resultado do teste:"
            echo "$TEST_RESULT"
            echo "✅ API está funcionando corretamente!"
            API_OK=1
            break
        else
            echo "⚠️ API retornou resposta vazia na tentativa $retry."
        fi
    else
        echo "⚠️ API não respondeu na tentativa $retry. Aguardando mais 10 segundos..."
        sleep 10
    fi
done

if [ -z "$API_OK" ]; then
    echo "❌ Falha na API após 3 tentativas. Verificando logs completos:"
    cd docker
    docker compose logs || docker-compose logs
    cd ..
fi

# Testar se a interface web está funcionando
echo "🔍 Testando a interface web..."
for retry in {1..3}; do
    if curl -s http://localhost:5000 > /dev/null; then
        echo "✅ Interface web está online em http://localhost:5000"
        WEB_OK=1
        break
    else
        echo "⚠️ Interface web não respondeu na tentativa $retry. Aguardando mais 5 segundos..."
        sleep 5
    fi
done

if [ -z "$WEB_OK" ]; then
    echo "❌ Falha na interface web após 3 tentativas. Verificando logs completos:"
    cd docker
    docker compose logs || docker-compose logs
    cd ..
fi

# Mostrar comandos úteis
echo "📊 Container Docker rodando com:"
echo "- API: http://localhost:7100"
echo "- Interface Web: http://localhost:5000"
echo ""
echo "Comandos úteis:"
echo "- Ver logs: cd docker && docker compose logs -f"
echo "- Reiniciar: cd docker && docker compose restart"
echo "- Reiniciar apenas API: docker exec -it api-classificacao pm2 restart api-classificacao"
echo "- Parar: cd docker && docker compose down" 