FROM python:3.9-slim

WORKDIR /app

# Instalar PM2 (requer Node.js)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install pm2 -g && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação com a nova estrutura
COPY src/ /app/src/
COPY data/ /app/data/
COPY scripts/ /app/scripts/
COPY main.py /app/
COPY docker/process.json /app/

# Copiar o modelo para a raiz do container
COPY src/model/modelo_classificacao.pkl /app/modelo_classificacao.pkl

# Portas que serão expostas (API e Interface Web)
EXPOSE 7100 5000

# Criar diretório para volume de dados
RUN mkdir -p /app/data

# Definir healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python /app/scripts/healthcheck.py || exit 1

# Tornar os scripts executáveis
RUN chmod +x /app/scripts/healthcheck.py

# Criar um script de inicialização para o PM2
RUN echo '#!/bin/bash\ncd /app\n\n# Garantir que o modelo seja gerado e treinado\npython -m src.model.gerador_dados_sinteticos\npython -m src.model.treinar_modelo\n\n# Copiar o modelo para a raiz do container (garantir que está disponível)\ncp /app/src/model/modelo_classificacao.pkl /app/modelo_classificacao.pkl\n\n# Iniciar os serviços\npm2-runtime start process.json' > /app/start.sh && \
    chmod +x /app/start.sh

# Comando para inicialização
CMD ["/app/start.sh"] 