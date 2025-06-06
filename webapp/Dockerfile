FROM node:18-alpine3.18 as builder
WORKDIR '/app'
COPY package*.json ./
RUN npm ci
COPY . .
RUN npx ng build
FROM nginx
EXPOSE 80
COPY --from=builder /app/dist/test /usr/share/nginx/html
COPY /nginx.conf /etc/nginx/conf.d/default.conf
