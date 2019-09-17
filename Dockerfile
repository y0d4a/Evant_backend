FROM python:3.6.8
MAINTAINER Your Name "agatha@alterra.id"
RUN mkdir -p /backend/rest_svc
COPY . /backend/rest_svc
RUN pip install -r /backend/rest_svc/requirements.txt
WORKDIR /backend/rest_svc
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
