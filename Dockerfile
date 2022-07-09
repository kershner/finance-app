# Dockerfile

FROM python:3.7

# install nginx
RUN apt-get update && apt-get install nginx nano -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source
RUN mkdir -p opt/finance_by_month
RUN mkdir -p opt/finance_by_month/pip_cache
COPY . opt/finance_by_month

# install python requirements and run django admin commands
WORKDIR opt/finance_by_month
RUN pip install -r requirements.txt --cache-dir pip_cache
RUN python manage.py collectstatic --noinput

# set file system permissions for our root directory
RUN chown -R www-data:www-data /opt/finance_by_month

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ./start_server.sh