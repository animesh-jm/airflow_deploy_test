from airflow.models import DAG
from airflow.contrib.operators.aws_athena_operator import AWSAthenaOperator
from datetime import datetime
#from airflow.providers.amazon.aws.operators.athena
from datetime import timedelta
from airflow.hooks.S3_hook import S3Hook

default_args = {
    'owner': 'bet369',
    'depends_on_past': False,
    'start_date': datetime(2019, 12, 5),
    'email': ['jobbing.314@gmail.com'],
    'email_on_failure': ['jobbing.314@gmail.com'],
    'email_on_retry': ['jobbing.314@gmail.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
    #, 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


with DAG(dag_id='bet369_firstpart_goals_month'
         ,schedule_interval="@monthly"
         ,start_date=datetime(2019, 12, 5)
		 #,template_searchpath = ['./sqls/']
		 ,default_args=default_args) as dag:
		 
	#need to include the load partitions of minutssss
    refresh_minuts = AWSAthenaOperator(
        task_id='refresh_parts_minuts_info',
        query="MSCK REPAIR TABLE sampledb.minuts_info;",
		output_location='s3://matchestest/airflow_athena/logs',
        database='sampledb'
    )
	
    drop_tmp_minuts_info0 = AWSAthenaOperator(
        task_id='00_drop_tmp_minuts_info',
        query="DROP TABLE IF EXISTS sampledb.TMP_MONTH_NODUPS;",
		output_location='s3://matchestest/airflow_athena/logs',
        database='sampledb'
    )
	
    tmp_minuts_info0 = AWSAthenaOperator(
        task_id='00_tmp_minuts_info',
        query="/sqls/00_month_tmp_minuts_info.sql",
		output_location='s3://matchestest/airflow_athena/logs',
        database='sampledb'
    )


    refresh_minuts >> drop_tmp_minuts_info0 >> tmp_minuts_info0