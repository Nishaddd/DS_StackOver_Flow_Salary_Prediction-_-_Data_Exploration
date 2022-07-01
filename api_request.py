import requests
import api


def curr_converter():
    USD = "USD"
    INR = "INR"


    url = f"https://api.apilayer.com/fixer/latest?symbols={INR}&base={USD}"

    payload = {}
    headers = {
        "apikey": api.API
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code

    result = response.json()
    rate = result['rates']["INR"]
    return float(rate),int(status_code)

curr_converter()