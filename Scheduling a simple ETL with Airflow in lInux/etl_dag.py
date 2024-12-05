 from airflow import DAG 

from airflow.operators.bash import BashOperator

from datetime import datetime,timedelta


default_args ={

	'owner' : 'airflow',

	'depends_on_past': False,

	'email_on_failure' : False,

	'email_on_retries' : False,

	'retries' : 1,

	'retry_delay': timedelta(minutes = 1),

	}

	

dag = DAG(

	'MYSQL_DAG', #dag name

	default_args = default_args,

	description = ' A simple  etl dag',

	schedule_interval = timedelta(minutes = 5),

	start_date = datetime(2024,12,5),

	catchup = False,

)


run_etl = BashOperator(

	task_id = 'run_etl',

	bash_command = 'bash /home/user/wrapper_script.sh ',

        dag = dag,

) 