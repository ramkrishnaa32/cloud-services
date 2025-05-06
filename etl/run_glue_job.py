import boto3
import time

# Replace with your job name
glue_job_name = 'csv_to_parquet'

# Optional: Define any job parameters if needed
job_arguments = {
    # '--arg1': 'value1',
    # '--arg2': 'value2'
}

# Initialize the boto3 Glue client
glue = boto3.client('glue', region_name='us-east-1')

# Start the Glue job
response = glue.start_job_run(
    JobName=glue_job_name,
    Arguments=job_arguments
)

job_run_id = response['JobRunId']
print(f"Glue job started with JobRunId: {job_run_id}")

# Monitor the job until it completes
while True:
    job_status = glue.get_job_run(JobName=glue_job_name, RunId=job_run_id)['JobRun']['JobRunState']
    print(f"Job status: {job_status}")
    if job_status in ['SUCCEEDED', 'FAILED', 'STOPPED']:
        break
    time.sleep(15)

print(f"Final job status: {job_status}")
