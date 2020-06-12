# cd /home/QNET.QUALNET.ORG/ek1815/swagger/iqies-security/swagger 
# sudo docker image build -t swagger-local:latest /home/QNET.QUALNET.ORG/ek1815/swagger/iqies-security/swagger 
# sudo docker image ls
# sudo docker run -p 4500:4500 swagger-local:latest
# sudo docker run -p 4600:8080 -e API_URL="http://10.137.177.242:4500/patientassessmenthha.json" swaggerapi/swagger-ui
# From browser do http://10.137.177.242:4600/

FROM node:14.4.0-slim

# Create app directory
WORKDIR /swagger
ADD getOpenApiJson.sh /swagger
CMD chmomd +x /swagger/getOpenApiJson.sh
RUN apt-get update
RUN apt-get -y install -y procps

RUN apt-get -y install cron
COPY myCron /etc/cron.d/myCron
RUN chmod 0744 /etc/cron.d/myCron
RUN crontab /etc/cron.d/myCron
RUN touch /var/log/cron.log
#CMD cron

RUN apt-get -y install python3.5
CMD python3.5 --version

RUN apt-get -y install curl
RUN /swagger/getOpenApiJson.sh
RUN npm install -g http-server
EXPOSE 4500
CMD cron && http-server --port 4500 --cors
