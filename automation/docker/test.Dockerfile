FROM node:8.11.1-alpine
# Create app directory
WORKDIR /app
# Install app dependencies
COPY . .
RUN yarn install
# Bundle app source
CMD [ "yarn", "start" ]
