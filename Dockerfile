FROM nginx:alpine

# Copy the HTML file as index.html so it loads at /
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

# nginx:alpine already has a CMD that starts nginx in foreground