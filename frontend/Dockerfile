# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
RUN mkdir doc_int
COPY docs/ doc_int
COPY frontend/package*.json ./
RUN npm install
COPY frontend/. ./
RUN npm run build
CMD cp -r build result_build \
    && cp -r doc_int docs