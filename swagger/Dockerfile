# cd /home/QNET.QUALNET.ORG/ek1815/development
# sudo docker image build -t swagger-local:latest /home/QNET.QUALNET.ORG/ek1815/development
# sudo docker image ls
# sudo docker run -p 4500:4500 swagger-local:latest
# sudo docker run -p 4600:8080 -e API_URL="http://10.137.177.242:4500/patientassessmenthha.json" swaggerapi/swagger-ui
# From browser do http://10.137.177.242:4600/

FROM node:14.4.0-slim

# Create app directory
WORKDIR /usr/src/app
ADD getOpenApiJson.sh /usr/src/app/
CMD chmomd +x /usr/src/app/getOpenApiJson.sh
RUN apt-get update
RUN apt-get install -y procps
RUN apt-get -y install python3.5
CMD python3.5 --version

RUN apt-get -y install curl
RUN /usr/src/app/getOpenApiJson.sh
RUN npm install -g http-server
EXPOSE 4500
CMD http-server --port 4500 --cors
