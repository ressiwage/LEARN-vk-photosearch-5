FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
