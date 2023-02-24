FROM python:slim

RUN useradd -m appuser
USER appuser
WORKDIR /chatbot
ENV PATH="/home/appuser/.local/bin:$PATH"
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--timeout", "200", "--worker-class", "gevent"]