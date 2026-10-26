FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DB_PATH=/app/data/db.sqlite3
WORKDIR /app
COPY requirements.txt /app/
COPY wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels \
    && useradd --create-home appuser \
    && mkdir -p /app/data \
    && chown appuser:appuser /app/data
COPY --chown=appuser:appuser manage.py entrypoint.sh /app/
COPY --chown=appuser:appuser app1 /app/app1
COPY --chown=appuser:appuser website /app/website
COPY --chown=appuser:appuser templates /app/templates
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)"
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
