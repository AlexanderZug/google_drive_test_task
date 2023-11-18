FROM python:3.11-alpine3.16
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
COPY app /app
EXPOSE 8000
CMD ["gunicorn", "export_to_google_drive.wsgi:application", "--bind", "0:8000" ]
