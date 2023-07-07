FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

COPY team_stats_domain_service/requirements.txt ./

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY team_stats_domain_service $APP_HOME/team_stats_domain_service

CMD ["uvicorn", "team_stats_domain_service.main:app", "--host", "0.0.0.0", "--port", "8080"]
