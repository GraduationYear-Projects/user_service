FROM python:3.9-slim-buster AS builder

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: Final Minimal Image ----------
FROM python:3.9-slim-buster

WORKDIR /app

# Copy only installed packages from the builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only necessary application files
COPY app.py .
COPY user/ ./user/

# Clean up unnecessary files and directories
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find /usr/local/lib/python3.9/site-packages -type d -name "tests" -exec rm -rf {} + && \
    find /usr/local/lib/python3.9/site-packages -type d -name "test" -exec rm -rf {} + && \
    find /usr/local/lib/python3.9/site-packages -type f -name "*.pyc" -delete && \
    find /usr/local/lib/python3.9/site-packages -type f -name "*.pyo" -delete

CMD ["python", "app.py"]
