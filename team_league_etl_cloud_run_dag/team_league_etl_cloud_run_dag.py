import json

import airflow
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

from team_league_etl_cloud_run_dag.settings import Settings

settings = Settings()

with airflow.DAG(
        "team_league_etl_cloud_run_dag",
        default_args=settings.dag_default_args,
        schedule_interval=None) as dag:
    print_token = BashOperator(
        task_id="print_token",
        bash_command=f'gcloud auth print-identity-token "--audiences={settings.team_stats_service_url}"'
    )

    token = "{{ task_instance.xcom_pull(task_ids='print_token') }}"

    run_cloud_run_service = SimpleHttpOperator(
        task_id="run_cloud_run_service",
        method="POST",
        http_conn_id="team_stats_service",
        endpoint=settings.team_stats_service_post_endpoint,
        data=json.dumps(settings.team_stats_service_slogans_request_body),
        headers={"Authorization": "Bearer " + token},
    )

    move_file_to_cold = GCSToGCSOperator(
        task_id="move_file_to_cold",
        source_bucket=settings.team_stats_source_bucket,
        source_object=settings.team_stats_source_object,
        destination_bucket=settings.team_stats_dest_bucket,
        destination_object=settings.team_stats_dest_object,
        move_object=False
    )

    print_token >> run_cloud_run_service >> move_file_to_cold
