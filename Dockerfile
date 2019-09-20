FROM python:3.6
MAINTAINER Your Name "agatha@alterra.id"
RUN mkdir -p /backend/rest_svc
COPY . /backend/rest_svc
RUN pip install -r /backend/rest_svc/requirements.txt
# RUN cd /backend/rest_svc/
# RUN export FLASK_ENV=testing
# RUN cd ../../
# RUN pytest --cov=blueprints /backend/rest_svc/tests
# RUN cd /backend/rest_svc/
# RUN export FLASK_ENV=development
# RUN cd ../../
WORKDIR /backend/rest_svc
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
