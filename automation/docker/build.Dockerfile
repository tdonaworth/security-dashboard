FROM node:8.11.1-alpine

ENV NODE_ENV production
ARG DATABASE_URL
ARG SERVICE_NAME
LABEL ANONYMOUS 1
LABEL EXPORT_ENV_VARS=1
LABEL SERVICE_NAME=${SERVICE_NAME}
LABEL API_NAME=${SERVICE_NAME}
# Create app directory
WORKDIR /opt
# Install dependencies, build app
COPY . .
RUN yarn --prod=false
# This includes seeders, fine for sandbox but not higher envs
RUN env DATABASE_URL=${DATABASE_URL} yarn migrate up
# Prune to prod dependencies
RUN yarn --prod=true

COPY automation/docker/env_export.sh ./
RUN chmod +x ./env_export.sh

EXPOSE 8080

ENTRYPOINT ["./env_export.sh"]
CMD [ "yarn", "start" ]
