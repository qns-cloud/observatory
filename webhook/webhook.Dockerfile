ARG PYTHON_VER=3.10

FROM python:${PYTHON_VER}-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 9997

# Run the application
CMD ["python", "-m", "app.main"]