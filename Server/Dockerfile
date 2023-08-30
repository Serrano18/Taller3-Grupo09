# Usa la imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos y el código de la aplicación al contenedor
COPY requirements.txt .
COPY app.py .

# Instala las dependencias de la aplicación
RUN pip install -r requirements.txt

# Expone el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
