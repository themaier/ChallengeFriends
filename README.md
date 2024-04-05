# Challenge-Accepted

## Start Challenge-Accepted:

Getting started:

1. Install:

   - VSCode
   - WSL2
   - DockerDesktop
   - create .env in backend-folder !!!!!!!!!!!!!!!

2. In Terminal in Challenge-Accepted root directory
   - docker-compose build
   - docker-compose up

Backend (Swagger) now runs on:

- http://localhost:8000/docs

Frontend now runs on:

- http://localhost:3000/

Database Connection if needed:

- http://localhost:5050/
- database: db_service
- pw: password

Strg + C/docker-compose down to stop

For more help with the docker commands, have a look at our HELP.md

## Deployed Release

- There is also a deployed version of the Challenge-Accepted.
- You can find it under: http://18.196.97.249:3000
- Also every time something is merge into main, it gets deployed automatically
  through a gitub actions script that copies over the contend and user docker-compose up
  to start the services.

## Start Challenge-Accepted without docker-compose (optional):

cd backend

- uvicorn src.main:app
- http://127.0.0.1:8000/docs

frontend:

- cd frontend
- npm install
- npm run dev
- http://127.0.0.1:3000

### install dev software backend:

Install postgreSQL on your computer
Open pgadmin -> create db with name challenge-accepted
host name/address = db_service
Put your password and username into backend/src/db/local.env !

## Access AWS EC2 instance:

- ssh -i Challenge-Accepted.pem ubuntu@ec2-18-196-97-249.eu-central-1.compute.amazonaws.com
- Challenge-Accepted.pem is needed
