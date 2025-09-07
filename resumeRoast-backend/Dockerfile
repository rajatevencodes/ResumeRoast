# =====================================================================================
# Stage 1: Builder
# =====================================================================================
FROM python:3.12-slim-bookworm AS builder

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files.
# PYTHONUNBUFFERED: Ensures logs are sent straight to the terminal without buffering.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# /opt - optinal directory - Not Part of the default operating system
RUN python -m venv /opt/venv
# Activate the virtual environment for subsequent commands (pip install) in this stage.
ENV PATH="/opt/venv/bin:$PATH"
# Upgrade pip within the virtual environment
RUN pip install --upgrade pip 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =====================================================================================
# Stage 2: Final Image
# =====================================================================================
FROM python:3.12-slim-bookworm
# Set the working directory inside the container
WORKDIR /app
# Set environment variables again for the final image
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# poppler-utils - PDF to image conversion
RUN apt-get update && \
    apt-get install -y --no-install-recommends poppler-utils curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the virtual environment with installed packages from the 'builder' stage.
COPY --from=builder /opt/venv /opt/venv
COPY ./src /app
# TODO : Avoid this :) But currently needed this for OPENAI API key
COPY .env /app/.env
# For Workers
COPY production.sh /app/production.sh
RUN chmod +x ./production.sh
EXPOSE 8000
CMD ["/app/production.sh"]