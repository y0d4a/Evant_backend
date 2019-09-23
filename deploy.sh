sudo docker stop backend
sudo docker rm backend
sudo docker rmi agatharach/backend-project
sudo docker run -d --name backend -p 5000:5000 agatharach/backend-project:latest



