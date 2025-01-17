import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import time

DEALERSHIP_BASE_URL = "https://parthshah347-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
REVIEWS_BASE_URL = 'https://parthshah347-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={dealer_id}'
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    response = None  # Initialize response variable

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

    if response is not None:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    else:
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print('PAYLOAD: ', payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
   
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    # print('json_result from line 31', json_result)    

    if json_result:
        # Get the row list in JSON as dealers
        # print("63 - RA",json_result)
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"], 
                city=dealer_doc["city"],
                dealer_id=dealer_doc["id"], 
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"], 
                full_name=dealer_doc["full_name"], 
                short_name=dealer_doc["short_name"],                                
                st=dealer_doc["st"], 
                zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results



def get_dealer_by_id(url, dealer_id):
    # url = REVIEWS_BASE_URL.format(dealer_id=dealer_id)
    url = url + f'?id={dealer_id}'
    json_result = get_request(url)
    # print('json_result from line 98', json_result)
    # print('get_dealer_by_id_from_cf URL IS: ', url)
    if json_result:
        dealer = json_result
        # Create a CarDealer object with values in `dealer` dictionary
        dealer_obj = CarDealer(
            address=dealer.get("address", ""),
            city=dealer.get("city", ""),
            full_name=dealer.get("full_name", ""),
            dealer_id=dealer.get("id", ""),
            lat=dealer.get("lat", ""),
            long=dealer.get("long", ""),
            short_name=dealer.get("short_name", ""),
            st=dealer.get("st", ""),
            zip=dealer.get("zip", "")
        )
    return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(dealer_id):
    # Call get_request with the base URL for reviews and dealerId parameter
    url = REVIEWS_BASE_URL.format(dealer_id=dealer_id)
    # Pass the API key to the get_request function
    api_key = "4XjngQA0CruDZEjW5OwF1A6GJf-BZ80IXxWSWgHQ-2A2"
    json_result = get_request(url)
    # print('json_result from line 131', json_result)
    results = []
    if json_result:
        for review_data in json_result:
            # Check if all required fields exist in review_data
            if "id" in review_data and "dealership" in review_data and "review" in review_data \
                    and "purchase" in review_data and "purchase_date" in review_data \
                    and "car_make" in review_data and "car_model" in review_data and "car_year" in review_data:
                # If all fields are available, create the DealerReview object
                dealer_review = DealerReview(
                    review_id=review_data["id"],
                    dealer_id=review_data["dealership"],
                    review=review_data["review"],
                    purchase=review_data["purchase"],
                    purchase_date=review_data["purchase_date"],
                    car_make=review_data["car_make"],
                    car_model=review_data["car_model"],
                    car_year=review_data["car_year"],
                    sentiment=None
                )
                results.append(dealer_review)
    # print('RESULTS: ', results)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    API_KEY = "VDVaU-BfB7OQ-brh7AxEgko5XGgzVEu0hoCjgoPjDM1t"
    NLU_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/d49b5692-b408-4810-b2cd-6f87829466aa'
    dealer_review = dealer_review.review
   
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    response = natural_language_understanding.analyze(
        text=dealer_review,
        language='en',
        features=Features(
        sentiment=SentimentOptions())).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)

