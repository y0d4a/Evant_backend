sudo docker stop backend-evant
sudo docker rm backend-evant
sudo docker rmi agatharach/backend-evant
sudo docker run -d --name backend -p 5000:5000 agatharach/backend-evant:latest



