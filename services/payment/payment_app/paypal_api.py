import json

import requests
from fastapi import HTTPException
from os import environ as env

from payment_app import schemas

BASE_URL = env.get('BASE_URL')
CLIENT_ID = env.get('CLIENT_ID')
CLIENT_SECRET = env.get('CLIENT_SECRET')


def get_papal_access_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    try:
        response = requests.post(f'{BASE_URL}v1/oauth2/token', headers=headers, data=data, auth=auth)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

        # Handle connection errors and other issues
        raise HTTPException(status_code=500, detail=f"An error occurred while getting the paypal access token")


def create_paypal_order(order: schemas.OrderSchemaForPaypal):
    payload = get_papal_access_token()
    token = payload.get('access_token')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": order.total_price,
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": order.total_price
                        }
                    }

                },
                "items": [
                    {
                        "name": item.name,
                        "quantity": item.quantity,
                        "unit_amount": {
                            "currency_code": "USD",
                            "value": item.unit_amount_value
                        }

                    } for item in order.items
                ]

            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "brand_name": "EXAMPLE INC",
                    "locale": "en-US",
                    "return_url": "http://localhost:8005/auto-capture-payment-after-approval",
                    "cancel_url": "https://example.com/cancelUrl"
                }
            }
        }
    }
    try:
        response = requests.post(f'{BASE_URL}v2/checkout/orders/', headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

        # Handle connection errors and other issues
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the paypal order")


def capture_payment(paypal_order_id: str):
    payload = get_papal_access_token()
    token = payload.get('access_token')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    try:
        response = requests.post(f'{BASE_URL}v2/checkout/orders/{paypal_order_id}/capture', headers=headers)
        print(response.text)
        if response.status_code == 201:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

        raise HTTPException(status_code=500, detail=f"An error occurred while capturing the payment")
