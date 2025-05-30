import json
import boto3
import time

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

emr = boto3.client('emr', region_name='us-east-1')

cluster_config = load_json('../configs/cluster_config.json')
bootstrap_actions = load_json('../configs/bootstrap_actions.json')
log_config = load_json('../configs/logging_config.json')
steps_config = load_json('../configs/steps_config.json')
roles = load_json('../configs/emr_roles.json')

response = emr.run_job_flow(
    Name=cluster_config["Name"],
    ReleaseLabel=cluster_config["ReleaseLabel"],
    Applications=cluster_config["Applications"],
    Instances=cluster_config["Instances"],
    BootstrapActions=bootstrap_actions,
    Steps=steps_config,
    JobFlowRole=roles["JobFlowRole"],
    ServiceRole=roles["ServiceRole"],
    LogUri=log_config["LogUri"],
    VisibleToAllUsers=cluster_config["VisibleToAllUsers"]
)

print("Cluster created with ID:", response['JobFlowId'])

cluster_id = response['JobFlowId']
print(f"Monitoring cluster: {cluster_id}")

# Wait until the cluster is running
while True:
    cluster_desc = emr.describe_cluster(ClusterId=cluster_id)
    state = cluster_desc['Cluster']['Status']['State']
    print(f"Cluster status: {state}")

    if state in ['WAITING', 'RUNNING', 'TERMINATING', 'TERMINATED', 'TERMINATED_WITH_ERRORS']:
        break
    time.sleep(30)

# Monitor steps
steps = emr.list_steps(ClusterId=cluster_id)['Steps']
step_ids = [step['Id'] for step in steps]

print("Monitoring step execution...")
step_statuses = {step_id: 'PENDING' for step_id in step_ids}

while True:
    all_done = True
    for step_id in step_ids:
        step = emr.describe_step(ClusterId=cluster_id, StepId=step_id)
        status = step['Step']['Status']['State']
        step_statuses[step_id] = status
        if status not in ['COMPLETED', 'FAILED', 'CANCELLED']:
            all_done = False
    print("Current step statuses:", step_statuses)
    if all_done:
        break
    time.sleep(30)

# Final summary
print("\n Step Execution Summary:")
for step_id, status in step_statuses.items():
    print(f"Step {step_id}: {status}")
