FROM python:3-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

COPY src/app.py /app/app.py
COPY src/game.py /app/game.py

EXPOSE 8050

ENTRYPOINT ["python"]

CMD ["/app/app.py"]