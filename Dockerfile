FROM python:3.9
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    vim

ENV PYTHONUNBUFFERED=1

WORKDIR /code/
ADD . /code

RUN pip install -r requirements.txt


# Server

EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["gunicorn", "base.wsgi:application", "--bind", "0.0.0.0:8000"]