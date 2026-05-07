FROM python:3.11-slim

WORKDIR /app

# Install API + engine dependencies
COPY api/requirements-api.txt /tmp/requirements-api.txt
RUN pip install --no-cache-dir -r /tmp/requirements-api.txt

# Copy the engine + atlas data + cohort
COPY personalized_risk.py ./
COPY v2.0_scored/ ./v2.0_scored/
COPY validation/ ./validation/
COPY delta_squared_v1/ ./delta_squared_v1/
COPY llms.txt ./
COPY api/ ./api/

EXPOSE 8000

# Single worker is fine for a free public API; Railway/Render will scale
# horizontally if traffic warrants. Determinism note: the engine is pure
# (no shared state across requests), so multiple workers are safe.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
