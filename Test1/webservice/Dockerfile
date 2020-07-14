FROM python:3.8.3-alpine3.12

# setup user
RUN adduser -D flasky
WORKDIR /home/flasky

# install curl
RUN apk update && \
    apk add curl

USER flasky

# copy code, certs
COPY --chown=flasky:flasky requirements requirements
COPY --chown=flasky:flasky certs certs
COPY --chown=flasky:flasky config.py es_helper.py user.py flasky.py boot.sh db.py security.py /home/flasky/
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

# runtime configuration
EXPOSE 5000
ENTRYPOINT ["/home/flasky/boot.sh"]
