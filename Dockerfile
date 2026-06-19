FROM python:3.11-slim

ARG BUILD_DIR
ARG PORT=8501
ENV PORT=${PORT}

WORKDIR /app

COPY ${BUILD_DIR}/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ${BUILD_DIR}/ .

EXPOSE ${PORT}

CMD sh -c "streamlit run app.py \
  --server.port=${PORT} \
  --server.headless=true \
  --server.address=0.0.0.0 \
  --server.enableCORS=false"
