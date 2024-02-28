# Use a imagem oficial do Python
FROM python:3.8-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY requirements.txt /app
COPY app.py /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta em que o aplicativo Flask será executado
EXPOSE 5000

# Comando para executar o aplicativo Flask
CMD ["python", "app.py"]