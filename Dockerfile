# Use official Python image
FROM python:3.12

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

RUN apt-get update && apt-get install -y ffmpeg


# Run gunicorn server (production)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
