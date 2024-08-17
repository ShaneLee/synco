# Build stage
FROM python:3.11-slim AS build-stage

WORKDIR /app

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./server/ .

RUN useradd -m synco_user
USER synco_user

# Run stage
FROM python:3.11-slim AS run-stage

WORKDIR /app

COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY --from=build-stage /app /app

USER synco_user

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# Test stage
FROM build-stage AS test-stage

WORKDIR /app

ENV PYTHONPATH=/app/src

CMD ["pytest", "--disable-warnings"]
