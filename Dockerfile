# Create optimized Dockerfile for Flask app
# - python:3.9-slim
# - multi-stage optional
# - cache dependencies using requirements.txt
# - non-root user
# - expose 5000
# - CMD python app.py
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]