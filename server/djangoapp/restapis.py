import json
import os
import requests
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

GET_DEALERSHIP_ACTION = ''.join(['https://us-south.functions.appdomain.cloud/api/v1/web/HunterSchwager_Final%20Project/CarDealership/get_dealerships'])

GET_REVIEWS_ACTION = ''.join(['https://us-south.functions.appdomain.cloud/api/v1/web/HunterSchwager_Final%20Project/CarDealership/get-reviews'])

WATSON_URL = ''.join(['https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/c008aa68-1634-4a30-8259-981c9bbf977c'])

WATSON_API_KEY = 'nbj6fo223FOo7gW_L0cHpR4_zaMv80O8A21RkxI04ecs'

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if 'api_key' in kwargs.keys():
            api_key = kwargs['api_key']
            del(kwargs['api_key'])
            response = requests.get(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                auth=HTTPBasicAuth('apikey', api_key),
                params=kwargs
                )
        else:
            response = requests.get(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                params=kwargs
                )
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        if 'api_key' in kwargs.keys():
            #api_key in params, use auth
            api_key = kwargs['api_key']
            del(kwargs['api_key'])
            response = requests.post(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                auth=HTTPBasicAuth('apikey', api_key),
                params=kwargs,
                json=json_payload
                )
        else:
            response = requests.post(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                params=kwargs,
                json=json_payload
                )
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    #print(response.text)
    #print(response.request.path_url)
    json_data = json.loads(response.text)
    return response.json()

def get_dealers_from_cf(url = GET_DEALERSHIP_ACTION, **kwargs):
    results = []
    json_result = get_request(url + '/dealership', **kwargs)
    if json_result:
        for dealer_doc in json_result:
            dealer_obj = CarDealer(
                id=dealer_doc["id"],
                address=dealer_doc.get("address"),
                city=dealer_doc.get("city"),
                full_name=dealer_doc.get("full_name"),
                lat=dealer_doc.get("lat"),
                long=dealer_doc.get("long"),
                short_name=dealer_doc.get("short_name"),
                st=dealer_doc.get("st"),
                zip=dealer_doc.get("zip"),  
            )
            results.append(dealer_obj)
    return results

def get_dealer_by_id(dealerId, url = GET_DEALERSHIP_ACTION):
    url = url + '/dealership'
    return get_dealers_from_cf(url, id = dealerId)[0]

def get_dealer_by_state(state, url = GET_DEALERSHIP_ACTION):
    url = url + '/dealership'
    return get_dealers_from_cf(url, state=state)

def get_dealer_reviews_from_cf(dealerId, url = GET_REVIEWS_ACTION):
    def json_to_dealer_review(data):
        return DealerReview(
            id=data.get('id', ''),
            dealership=data['dealership'],
            review=data['review'],
            name=data.get('name', ''),
            purchase=data.get('purchase', ''),
            purchase_date=data.get('purchase_date', ''),
            car_make=data.get('car_make', ''),
            car_model=data.get('car_model', ''),
            car_year=data.get('car_year', ''),
            sentiment=analyze_review_sentiments(text=data['review'])
            )
    url = url + '/review'
    json_result = get_request(url, dealerId=dealerId)
    if len(json_result) > 0:
        reviews = list(map(json_to_dealer_review, json_result))
        return reviews
    return []

def analyze_review_sentiments(**kwargs):
    URL = WATSON_URL + '/v1/analyze'
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = '2021-03-25'
    params["features"] = 'sentiment'
    params["return_analyzed_text"] = 'false'
    params["api_key"] = WATSON_API_KEY
    response = get_request(
        URL,
        **params
    )
    return response["sentiment"]["document"]["label"]