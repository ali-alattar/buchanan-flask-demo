FROM node:22-alpine AS frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/index.html frontend/vite.config.js ./
COPY frontend/src ./src
RUN npm run build

FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py opportunity_data.py scoring.py ./
COPY --from=frontend-build /frontend/dist ./frontend/dist

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
