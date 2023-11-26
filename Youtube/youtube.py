import threading
import requests
import api_client



def search(query: str) -> list:
    response = api_client.sendApiRequest(api_client.ApiControllers.Youtube, api_client.ApiRequests.Search, query)
    