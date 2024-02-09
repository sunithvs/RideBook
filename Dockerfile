FROM python:3

# Set environment variables for Python optimizations
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/

# Copy the project code into the container
COPY . /code/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install GDAL dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gdal-bin \
        libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Expose the port on which Gunicorn will run
EXPOSE 8000

# if production use gunicorn else use django server
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
