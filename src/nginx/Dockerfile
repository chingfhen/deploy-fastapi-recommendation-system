# Use an official Nginx image as the base image
FROM nginx:alpine

COPY /etc/letsencrypt/live/dsaichingfhen.com  /ssl


# Expose port 80 for the Nginx server
EXPOSE 80


CMD ["nginx", "-g", "daemon off;"]
