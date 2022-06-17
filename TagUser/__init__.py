import logging
import os
import azure.functions as func
import boto3
from botocore.exceptions import ClientError


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    username = req.params.get('username')
    tag = req.params.get('tag')
    if username and tag:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('Starting program')
        try:
            iam = boto3.client('iam',
                               aws_access_key_id=os.environ["AWS_AccessKeyId"],
                               aws_secret_access_key=os.environ["AWS_SecretAccessKey"])
            try:
                iam.tag_user(UserName=username, Tags=[tag])
            except iam.exceptions.NoSuchEntityException or iam.exceptions.LimitExceededException or \
                   iam.exceptions.InvalidInputException as err:
                return func.HttpResponse(str(err), status_code=400)
            except iam.exceptions.ServiceFailureException or iam.exceptions.ConcurrentModificationException as err:
                return func.HttpResponse(str(err), status_code=500)
            return func.HttpResponse("Successfully added tags.", status_code=200)
        except ClientError as err:
            return func.HttpResponse(str(err), status_code=400)
    else:
        return func.HttpResponse(
            "Please pass a username and tags on the query string",
            status_code=400
        )
