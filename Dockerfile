# Dockerfile

FROM python:3.7-slim

# install nginx
RUN apt-get update && apt-get install nginx -y --no-install-recommends

# copy source
RUN mkdir -p opt/finance_by_month
RUN mkdir -p opt/finance_by_month/pip_cache
COPY . opt/finance_by_month

# install python requirements
WORKDIR opt/finance_by_month
RUN pip install -r requirements.txt --cache-dir pip_cache

# expose port
EXPOSE 8020