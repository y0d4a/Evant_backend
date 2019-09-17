sudo docker stop agatharach/backend-project:latest
sudo docker rm agatharach/backend-project:latest
sudo docker rmi agatharach/backend-project
sudo docker run -d --name backend -p 5000:5000 agatharach/backend-project:latest



