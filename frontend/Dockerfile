FROM node:lts-alpine as build-stage

COPY package.json ./
WORKDIR /frontend
RUN npm install
COPY . .
# RUN npm run build
# EXPOSE 3000
# CMD ["npm", "run", "dev"]