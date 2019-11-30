FROM node:12

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
RUN npm install -g @angular/cli
RUN apt-get update && apt-get install nginx -y

COPY app .
COPY nginx/* /etc/nginx/sites-available/