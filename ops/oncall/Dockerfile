FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir httpx
COPY app.py .
EXPOSE 8099
CMD ["python", "app.py"]
