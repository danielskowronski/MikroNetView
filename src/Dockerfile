FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
  FLASK_ENV=production \
  FLASK_APP=app.py

RUN addgroup --system webgroup && adduser --system webuser --ingroup webgroup

WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app
RUN chown -R webuser:webgroup /app
RUN python3 -m wget -o /app/static/favicon.ico https://mikrotik.com/favicon.ico
USER webuser

EXPOSE 9001

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:9001", "app:app"]