FROM python:3.10-slim

# Set up non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set Hugging Face cache directory
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HOME=/app/cache
ENV HF_HUB_CACHE=/app/cache

# Set working directory
WORKDIR /app

# Copy files
COPY --chown=user . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port expected by HF Spaces
EXPOSE 7860

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
