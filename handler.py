import sys
from zipfile import ZipFile
from io import BytesIO

import boto3
from botocore.client import Config


def has_dir(z, name):
    return any(x.startswith("%s/" % name.rstrip("/")) for x in z.namelist())


def mark_complete(event):
    client = boto3.client('codepipeline')
    return client.put_job_success_result(
        jobId=event["CodePipeline.job"]["id"],
        executionDetails={
            'summary': 'Success',
            'percentComplete': 100
        }
    )


def mark_failed(event, message):
    client = boto3.client('codepipeline')
    return client.put_job_failure_result(
        jobId=event["CodePipeline.job"]["id"],
        failureDetails={
            'type': 'JobFailed',
            'message': message,
        })


def fetch_zip(event):
    s3_data = (
        event["CodePipeline.job"]["data"]
        ["inputArtifacts"][0]["location"]["s3Location"])

    try:
        s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
        artifact = s3.get_object(
            Bucket=s3_data["bucketName"], Key=s3_data["objectKey"])
        artifact_bytes = artifact["Body"].read()
        return BytesIO(artifact_bytes)
    except:
        exception = sys.exc_info()[0]
        mark_failed(event, "S3 Error: {}".format(exception))
        return False


def parse_zip(event, zip_fp):
    try:
        with ZipFile(zip_fp, 'r') as artifact_zip:
            if not has_dir(artifact_zip, "source_markdown"):
                mark_complete(event)
            else:
                return artifact_zip
    except:
        exception = sys.exc_info()[0]
        mark_failed(event, "ZipFile Error: {}".format(exception))
        return False


def generate_html_from_markdown(event, markdown):
    pass


def upload_html_to_s3(event, html_files):
    pass


def lambda_handler(event, context):
    zip_fp = fetch_zip(event)
    if not zip_fp:
        return False

    return True
