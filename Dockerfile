FROM python:3


COPY . /task_manager

WORKDIR /task_manager

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

CMD ["sh", "entrypoint.sh"]