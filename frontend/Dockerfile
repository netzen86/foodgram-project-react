# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
RUN mkdir docs
COPY docs/ add/docs
COPY frontend/package*.json .
RUN npm install
COPY . ./
RUN npm run build
RUN cp -r docs docs
CMD cp -r build result_build