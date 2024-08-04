# Use a imagem base oficial do FastAPI com Uvicorn e Gunicorn
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

# Copie os requisitos para o container
COPY requirements.txt ./

# Instale as dependências do projeto
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copie o código da aplicação para o container
COPY . .

COPY cipher.py /usr/local/lib/python3.9/site-packages/pytube/
COPY letsencrypt /etc/letsencrypt/live/hello-doc.enzosakamoto.com.br

# Exponha a porta 8000 para o serviço
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/etc/letsencrypt/live/hello-doc.enzosakamoto.com.br/privkey.pem", "--ssl-certfile", "/etc/letsencrypt/live/hello-doc.enzosakamoto.com.br/fullchain.pem"]