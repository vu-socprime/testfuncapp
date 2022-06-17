import logging
import os
import azure.functions as func
import boto3
from botocore.exceptions import ClientError


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    username = req.params.get('username')
    if username:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('Starting program')
        try:
            iam = boto3.client('iam',
                               aws_access_key_id=os.environ["AWS_AccessKeyId"],
                               aws_secret_access_key=os.environ["AWS_SecretAccessKey"])
            response_list = []
            paginator = iam.get_paginator('list_attached_user_policies')
            try:
                for response in paginator.paginate(UserName=username):
                    response_list.append(response["AttachedPolicies"])
                response_list = [response for sublist in response_list for response in sublist]
            except iam.exceptions.NoSuchEntityException or iam.exceptions.InvalidInputException as err:
                return func.HttpResponse(str(err), status_code=400)
            except iam.exceptions.ServiceFailureException as err:
                return func.HttpResponse(str(err), status_code=500)
            return func.HttpResponse(str(response_list), status_code=200)
        except ClientError as err:
            return func.HttpResponse(str(err), status_code=400)
    else:
        return func.HttpResponse(
            "Please pass a username on the query string",
            status_code=400
        )
