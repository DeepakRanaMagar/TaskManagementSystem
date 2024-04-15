FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# ENTRYPOINT ["python", "./manage.py"]
CMD ["python3","manage.py","runserver"]