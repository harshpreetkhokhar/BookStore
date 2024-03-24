import logging
import azure.functions as func
import os
from azure.cosmos import CosmosClient
# from azure.core.credentials import AzureKeyCredential
from azure.identity import ClientSecretCredential

connection_string = os.getenv('CosmosDbConnectionSetting') 
cosmos_client = CosmosClient.from_connection_string(connection_string)

# Initialize Cosmos DB client
database_name = "my-database"
container_name = "my-container"
container = cosmos_client.get_database_client(database_name).get_container_client(container_name)

def get_items(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Getting items from Cosmos DB.')
    items = list(container.read_all_items())
    return func.HttpResponse(body=str(items), status_code=200)

def add_item(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Adding item to Cosmos DB.')

    try:
        req_body = req.get_json()
        container.create_item(body=req_body)
        return func.HttpResponse("Item added successfully", status_code=201)
    except ValueError as ve:
        logging.error(f"ValueError occurred: {ve}")
        return func.HttpResponse("Invalid request body", status_code=400)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse("Internal server error", status_code=500)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method == "GET":
        return get_items(req)
    elif req.method == "POST":
        return add_item(req)
    else:
        return func.HttpResponse(
            "Invalid request method",
            status_code=405
        )