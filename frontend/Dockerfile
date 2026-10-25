# Multi-stage production build for Frontend
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci --prefer-offline --no-audit

COPY . .
ENV REACT_APP_API_BASE_URL=/api
RUN npm run build

# Stage 2: Minimal hardened Nginx runner
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
