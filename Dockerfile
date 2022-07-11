# Dockerfile

FROM python:3.7-slim

# install nginx
RUN apt-get update && apt-get install nginx dos2unix -y --no-install-recommends

# copy source
RUN mkdir -p opt/finance_by_month
RUN mkdir -p opt/finance_by_month/pip_cache
COPY . opt/finance_by_month

# run dos2unix to prevent line ending errors
RUN dos2unix opt/finance_by_month/docker_entrypoint.sh && apt-get --purge remove -y dos2unix

# set exec permissions on entrypoint
RUN chmod +x opt/finance_by_month/docker_entrypoint.sh

# install python requirements
WORKDIR opt/finance_by_month
RUN pip install -r requirements.txt --cache-dir pip_cache

# expose port
EXPOSE 8020