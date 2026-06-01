FROM nginx:alpine

# Copy the HTML file as index.html so it loads at /
COPY index.html /usr/share/nginx/html/index.html
COPY portage_salarial.html /usr/share/nginx/html/portage_salarial.html

EXPOSE 80

# nginx:alpine already has a CMD that starts nginx in foreground
