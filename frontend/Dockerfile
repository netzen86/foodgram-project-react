# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
RUN mkdir docs
COPY docs/ docs/
COPY frontend/package*.json ./
RUN npm install
COPY frontend/. ./
RUN npm run build
COPY docs/ docs/
CMD cp -r build result_build