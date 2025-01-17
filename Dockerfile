# Usa una imagen base con Python 3.10
FROM python:3.10-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app/mage

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r mage/requirements.txt

# Expone el puerto predeterminado que utiliza Mage AI
EXPOSE 6789

# Comando para iniciar Mage AI
CMD ["mage", "start", "mage"]

