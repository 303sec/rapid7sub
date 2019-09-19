#!/usr/bin/env python3
import argparse
import os
import sys
import csv
import boto3
import botocore
from retrying import retry

# configuration
awsaccesskeyid="your aws acces key id"
awssecretaccesskey="your aws secret key"
region="us-east-2" ## You can change region
s3_bucket = 'xyeleathena'       # S3 Bucket name
# configuration

s3_ouput  = 's3://'+ s3_bucket   # S3 Bucket to store results
database  = 'default'  # The database to which the query belongs

# init clients
athena = boto3.client('athena', region_name=region,aws_access_key_id=awsaccesskeyid,aws_secret_access_key= awssecretaccesskey)
s3     = boto3.resource('s3',aws_access_key_id=awsaccesskeyid,aws_secret_access_key= awssecretaccesskey)

@retry(stop_max_attempt_number = 10,
    wait_exponential_multiplier = 300,
    wait_exponential_max = 1 * 60 * 1000)
def poll_status(_id):
    result = athena.get_query_execution( QueryExecutionId = _id )
    state  = result['QueryExecution']['Status']['State']

    if state == 'SUCCEEDED':
        return result
    elif state == 'FAILED':
        return result
    else:
        raise Exception

def run_query(query, database, s3_output):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': s3_output,
    })

    QueryExecutionId = response['QueryExecutionId']
    result = poll_status(QueryExecutionId)

    if result['QueryExecution']['Status']['State'] == 'SUCCEEDED':
        s3_key = QueryExecutionId + '.csv'
        local_filename = QueryExecutionId + '.csv'

        # download result file
        try:
            s3.Bucket(s3_bucket).download_file(s3_key, local_filename)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
            else:
                raise

        # read file to array
        rows = []
        with open(local_filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)

        # delete result file
        if os.path.isfile(local_filename):
            os.remove(local_filename)

        return rows

if __name__ == '__main__':
    domain = sys.argv[1]
    query = ("SELECT * FROM rapid7_fdns_any WHERE name LIKE '%."+domain+"' AND date = (SELECT MAX(date) from rapid7_fdns_any)")
    result = run_query(query, database, s3_ouput)
    subdomains=[]
    for x in result:
        y = list(dict.fromkeys(x.items()))[1][1]
        subdomains.append(y)
        pass
    subdomains = list(dict.fromkeys(subdomains))
    for x in subdomains:
        print(x)
        pass
