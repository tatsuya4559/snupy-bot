FROM public.ecr.aws/lambda/python:3.10

WORKDIR /var/task/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY lib ./lib

CMD [ "app.lambda_handler" ]
