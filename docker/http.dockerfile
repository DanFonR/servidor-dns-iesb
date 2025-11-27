FROM node:18-alpine AS build

ARG HOSTNAME

WORKDIR /app
COPY package*.json ./
# use --legacy-peer-deps to avoid peer dependency resolution failures in CI/Docker
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
