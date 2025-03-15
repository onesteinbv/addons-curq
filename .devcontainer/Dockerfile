FROM python:3.11-bookworm

ENV PAGER=more

USER root
RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev libpq-dev g++ postgresql-client
RUN pip install --no-cache-dir git-aggregator==4.0.2 click==8.1.8 pre-commit==4.1.0
USER vscode
