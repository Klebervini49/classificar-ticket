FROM python:3.9-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ /app/src/
COPY main.py /app/

# Gerar e treinar o modelo durante construção da imagem
RUN mkdir -p /app/data
COPY data/ /app/data/

# Criar script para copiar o modelo se existir
RUN echo '#!/bin/bash\nif [ -f /app/src/model/modelo_classificacao.pkl ]; then\n  cp /app/src/model/modelo_classificacao.pkl /app/\nelse\n  echo "Modelo será gerado durante execução"\nfi' > /app/copy_model.sh \
    && chmod +x /app/copy_model.sh \
    && /app/copy_model.sh

# Expor portas
EXPOSE 7100
EXPOSE 5000

# Comando para iniciar serviços (sem PM2)
CMD python -m src.api.api_docker & python main.py app 