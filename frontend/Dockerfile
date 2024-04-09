FROM node:lts-alpine as build-stage

COPY package.json ./
WORKDIR /frontend
RUN npm install --omit=dev
COPY . .
# EXPOSE 3000
# CMD ["npm", "run", "dev"]