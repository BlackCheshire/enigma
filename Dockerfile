FROM python:3.12.2-slim

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN pip install pipenv

COPY . .
RUN pipenv install --deploy

EXPOSE 13337
ENTRYPOINT ["python", "-m", "enigma"]