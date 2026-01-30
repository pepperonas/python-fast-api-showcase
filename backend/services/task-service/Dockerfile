FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY services/task-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared libraries
COPY shared/ ./shared/

# Copy application code
COPY services/task-service/src/ ./src/

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8002

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
