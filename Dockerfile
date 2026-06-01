FROM nginx:alpine

# Copy the HTML file as index.html so it loads at /
COPY index.html /usr/share/nginx/html/index.html
COPY calculateur-salaire.html /usr/share/nginx/html/calculateur-salaire.html
COPY calculateur-portage.html /usr/share/nginx/html/calculateur-portage.html

EXPOSE 80

# nginx:alpine already has a CMD that starts nginx in foreground
