FROM python:3.11.9-alpine3.20 as builder-base

COPY requirements.txt .

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.11.9-alpine3.20

WORKDIR /app
COPY --from=builder-base /root/.local /root/.local
COPY ./src .
ENTRYPOINT ["python", "main.py"]
# ENTRYPOINT ["/root/.local/bin/uvicorn", "main:app" , "--port", "8080"]
# CMD ["/root/.local/bin/fastapi", "run", "app/main.py", "--port", "80"]
EXPOSE 80
