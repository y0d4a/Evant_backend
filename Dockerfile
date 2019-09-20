FROM python:3.6.8
MAINTAINER Your Name "agatha@alterra.id"
RUN mkdir -p /backend/rest_svc
COPY . /backend/rest_svc
RUN pip install -r /backend/rest_svc/requirements.txt
# RUN python /backend/rest_svc/app.py
RUN export FLASK_ENV=testing
RUN pytest --cov=blueprints /backend/rest_svc/tests
RUN export FLASK_ENV=development
WORKDIR /backend/rest_svc
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
