# Dockerfile

# 1. Usar una imagen base oficial de Python
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo
WORKDIR /usr/src/app

# 3. Instalar dependencias (copiando solo el archivo de requisitos primero para aprovechar el cache de Docker)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código de la aplicación
COPY ./app /usr/src/app/app

# 5. Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# 6. Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]