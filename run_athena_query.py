import boto3
import time
from lib import constants

def run_athena_query(database, query, output_location, region):
    # Set up the Athena client
    athena_client = boto3.client('athena', region_name=region)

    # Start the query
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': output_location}
    )

    query_execution_id = response['QueryExecutionId']
    print(f"Started Query Execution ID: {query_execution_id}")

    # Wait for the query to finish
    while True:
        result = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']

        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

        print("Query is still running...waiting 2 seconds...")
        time.sleep(2)

    # Check final status
    if status == 'SUCCEEDED':
        print("Query succeeded! Fetching results...")
        results = athena_client.get_query_results(QueryExecutionId=query_execution_id)

        # Print results
        for row in results['ResultSet']['Rows']:
            print(row)
    else:
        print(f"Query ended with status: {status}")

if __name__ == "__main__":
    # Required details
    DATABASE = constants.DATABASE
    S3_OUTPUT = constants.ATHENA_LOG
    QUERY = '''SELECT subject, round(avg(score), 2) as avgScore 
               FROM student_partitions
               GROUP BY subject
               ORDER BY avgScore DESC'''

    # Run the function
    run_athena_query(constants.DATABASE, QUERY, S3_OUTPUT, constants.REGION)
