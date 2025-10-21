# Imagem base do Python 3.10
FROM python:3.10-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala cliente Firebird
RUN apt-get update && apt-get install -y libfbclient2 && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY ../exporter/ exporter/
COPY ../config/ config/

# Expõe a porta usada pelo Exporter
EXPOSE 8000

# Comando padrão para iniciar o Exporter
CMD ["python", "exporter/main.py"]
