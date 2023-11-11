FROM public.ecr.aws/lambda/python:3.10

WORKDIR /var/task/

COPY requirements.txt .

# HACK: ここでinstallするboto3を優先して見てほしいのでカレントディレクトリに入れておく
RUN pip install --no-cache-dir -r requirements.txt -t .

COPY app.py .
COPY lib ./lib

CMD [ "app.lambda_handler" ]
