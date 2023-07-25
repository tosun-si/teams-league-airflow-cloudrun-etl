# teams-league-airflow-cloudrun-etl

This project shows a real world use case with ETL batch pipeline using Cloud Storage, Cloud Run Service and BigQuery
orchestrated by Cloud Composer / Airflow

![etl_batch_pipeline_composer_cloudrun_bq.png](diagram%2Fetl_batch_pipeline_composer_cloudrun_bq.png)

The article on this topic :

https://medium.com/google-cloud/etl-batch-pipeline-with-cloud-storage-cloud-run-and-bigquery-orchestrated-by-airflow-composer-3cbb252b56aa

The video in English :

https://youtu.be/J6rIzvMzIfY

The video in French :

https://youtu.be/TPPJdzjglGM


## Build the container for Cloud Run Service with Cloud Build

Update `GCloud CLI` :

```bash
gcloud components update
```

Execute the following commands :

```bash
export PROJECT_ID=$(gcloud config get-value project)
export SERVICE_NAME=load-and-transform-team-stats-to-bq-service

gcloud builds submit --tag europe-west1-docker.pkg.dev/${PROJECT_ID}/internal-images/${SERVICE_NAME}:latest ./team_league_etl_cloud_run_dag/service
```

## Deploy the container image to Cloud Run

```bash
gcloud run deploy ${SERVICE_NAME} \
  --image europe-west1-docker.pkg.dev/${PROJECT_ID}/internal-images/${SERVICE_NAME}:latest \
  --region=${LOCATION}
```

The same with yaml file :

```bash
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config deploy-cloud-run-service.yaml \
    --substitutions _REPO_NAME="$REPO_NAME",_SERVICE_NAME="$SERVICE_NAME",_DOCKER_FILE_PATH="$DOCKER_FILE_PATH",_IMAGE_TAG="$IMAGE_TAG",_OUTPUT_DATASET="$OUTPUT_DATASET",_OUTPUT_TABLE="$OUTPUT_TABLE",_INPUT_BUCKET="$INPUT_BUCKET",_INPUT_OBJECT="$INPUT_OBJECT" \
    --verbosity="debug" .
```

Execution with a Cloud Build manual trigger :

```bash
gcloud beta builds triggers create manual \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="deploy-cloud-run-service-team-stats" \
    --repo="https://github.com/tosun-si/teams-league-airflow-cloudrun-etl" \
    --repo-type="GITHUB" \
    --branch="main" \
    --build-config="deploy-cloud-run-service.yaml" \
    --substitutions _REPO_NAME="$REPO_NAME",_SERVICE_NAME="$SERVICE_NAME",_DOCKER_FILE_PATH="$DOCKER_FILE_PATH",_IMAGE_TAG="$IMAGE_TAG",_OUTPUT_DATASET="$OUTPUT_DATASET",_OUTPUT_TABLE="$OUTPUT_TABLE",_INPUT_BUCKET="$INPUT_BUCKET",_INPUT_OBJECT="$INPUT_OBJECT" \
    --verbosity="debug"
```

## Deploy the Airflow DAG in Composer with Cloud Build from the local machine

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config deploy-airflow-dag.yaml \
    --substitutions _DAG_FOLDER="$DAG_FOLDER",_COMPOSER_ENVIRONMENT="$COMPOSER_ENVIRONMENT",_CONFIG_FOLDER_NAME="$CONFIG_FOLDER_NAME",_ENV="$ENV" \
    --verbosity="debug" .
```

Execution with a Cloud Build manual trigger :

```bash
gcloud beta builds triggers create manual \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="deploy-airflow-dag-team-stats" \
    --repo="https://github.com/tosun-si/teams-league-airflow-cloudrun-etl" \
    --repo-type="GITHUB" \
    --branch="main" \
    --build-config="deploy-airflow-dag.yaml" \
    --substitutions _DAG_FOLDER="$DAG_FOLDER",_COMPOSER_ENVIRONMENT="$COMPOSER_ENVIRONMENT",_CONFIG_FOLDER_NAME="$CONFIG_FOLDER_NAME",_ENV="$ENV" \
    --verbosity="debug"
```