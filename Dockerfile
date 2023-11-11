FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY app.py lib ${LAMBDA_TASK_ROOT}

CMD [ "app.lambda_handler" ]
