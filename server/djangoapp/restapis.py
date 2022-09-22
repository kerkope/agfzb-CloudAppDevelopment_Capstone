import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time

GET_ALL_DEALERSHIP_ACTION = 'https://us-south.functions.appdomain.cloud/api/v1/web/HunterSchwager_Final%20Project/CarDealership/get-all-dealerships'

GET_REVIEWS_ACTION = 'https://us-south.functions.appdomain.cloud/api/v1/web/HunterSchwager_Final%20Project/CarDealership/get-reviews'

WATSON_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/c008aa68-1634-4a30-8259-981c9bbf977c'

WATSON_API_KEY = 'nbj6fo223FOo7gW_L0cHpR4_zaMv80O8A21RkxI04ecs'


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

def get_dealers_from_cf(url = GET_ALL_DEALERSHIP_ACTION, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    if json_result:
        dealers = json_result['body']
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(
                address=dealer_doc["address"], 
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"], 
                id=dealer_doc["id"], 
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"],
                st=dealer_doc["st"], 
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results

def get_dealer_by_id(id, url = GET_ALL_DEALERSHIP_ACTION):
    url = url + '/dealership'
    return get_dealers_from_cf(url, id = id)[0]

def get_dealer_by_state(state, url = GET_ALL_DEALERSHIP_ACTION):
    url = url + '/dealership'
    return get_dealers_from_cf(url, state=state)

def get_dealer_reviews_from_cf(id, url = GET_REVIEWS_ACTION):
    def json_to_dealer_review(data):
        return DealerReview(
            id=data.get('id'),
            dealership=data.get('dealership'),
            review=data.get('review'),
            name=data.get('name'),
            purchase=data.get('purchase'),
            purchase_date=data.get('purchase_date'),
            car_make=data.get('car_make'),
            car_model=data.get('car_model'),
            car_year=data.get('car_year'),
            sentiment=analyze_review_sentiments(text=data['review'])
            )
    url = url + '/review'
    json_result = get_request(url, id=id)
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

def get_request(url, **kwargs):
    
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data