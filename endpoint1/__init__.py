import logging
import azure.functions as func
# import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    # res = requests.get('https://google.com')
    logging.info('Python HTTP trigger function processed a request.')
    # return func.HttpResponse(f'test response {res.status_code}')
    return func.HttpResponse('test response')
